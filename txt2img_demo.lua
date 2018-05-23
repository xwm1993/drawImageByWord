require 'image'
require 'nn'
require 'nngraph'
require 'cunn'
require 'cutorch'
require 'cudnn'
require 'lfs'
torch.setdefaulttensortype('torch.FloatTensor')

--构建字符表

local alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{} "
local dict = {}
for i = 1,#alphabet do
    dict[alphabet:sub(i,i)] = i
end

--结构翻转
ivocab = {}
for k,v in pairs(dict) do
  ivocab[v] = k
end
print(table.getn(ivocab))

opt = {
  dataset = 'cub',
  batchSize =48,        -- number of samples to produce
  noisetype = 'normal',  -- type of noise distribution (uniform / normal).
  imsize = 1,            -- used to produce larger images. 1 = 64px. 2 = 80px, 3 = 96px, ...
  noisemode = 'random',  -- random / line / linefull1d / linefull
  gpu = 1,               -- gpu mode. 0 = CPU, 1 = GPU
  display = 1,           -- Display image: 0 = false, 1 = true
  nz = 100,              
  doc_length = 201,
  queries = 'cub_queries.txt',
  net_gen = '',
  net_txt = '',
  net_des = '',
}

for k,v in pairs(opt) do opt[k] = tonumber(os.getenv(k)) or os.getenv(k) or opt[k] end
print(opt)
if opt.display == 1 then opt.display = true end

noise = torch.Tensor(opt.batchSize, opt.nz, opt.imsize, opt.imsize)
net_gen = torch.load(opt.net_gen)
net_des = torch.load(opt.net_des)
net_txt = torch.load(opt.net_txt)
if net_txt.protos ~=nil then net_txt = net_txt.protos.enc_doc end

net_gen:evaluate()
net_txt:evaluate()

-- 提取文本特征
local fea_txt = {}

-- 文本解码，构建词袋
local raw_txt = {}
local raw_img = {}
for query_str in io.lines(opt.queries) do
  local txt = torch.zeros(1,opt.doc_length,#alphabet)
  for t = 1,opt.doc_length do
    local ch = query_str:sub(t,t)
    local ix = dict[ch]
    if ix ~= 0 and ix ~= nil then
      txt[{1,t,ix}] = 1
    end
  end
  raw_txt[#raw_txt+1] = query_str
  --on gpu
  txt = txt:cuda()
  -- 生成的文本向量
  fea_txt[#fea_txt+1] = net_txt:forward(txt):clone()
end

if opt.gpu > 0 then
  require 'cunn'
  require 'cudnn' 
  net_gen:cuda()
  net_txt:cuda()
  net_des:cuda()
  noise = noise:cuda()
end
--local html = '<html><body><h1>Generated Images</h1><table border="1px solid gray" style="width=100%"><tr><td><b>Caption</b></td><td><b>Image</b></td></tr>'

for i = 1,#fea_txt do
  print(string.format('generating %d of %d', i, #fea_txt))
  --copy to matrix:batchSize*len(fea_txt)
  local cur_fea_txt = torch.repeatTensor(fea_txt[i], opt.batchSize, 1)
  --discribe text
  local cur_raw_txt = raw_txt[i]
  if opt.noisetype == 'uniform' then
    noise:uniform(-1, 1)
  elseif opt.noisetype == 'normal' then
    noise:normal(0, 1)
  end
  local images = net_gen:forward{noise, cur_fea_txt:cuda()}
  local scores = net_des:forward{images,cur_fea_txt:cuda()}
  print(scores)
  os.execute("rm -rf /home/alex/icml2016-master/results/image")
  local visdir = string.format('results/%s', opt.dataset)
  lfs.mkdir('results')
  lfs.mkdir(visdir)
  for j=1,images:size(1) do
     --local score=tostring(scores[j][1])
     local fname=string.format('%s/%e', visdir,scores[j][1])
     local fname_png = fname .. '-.png'
     image.save(fname_png, image.toDisplayTensor(images[j]))
  end
  --local fname = string.format('%s/img_%d', visdir, i)
  --local fname_png = fname .. '.png'
  --local fname_txt = fname .. '.txt'
  --local file=io.open(fname_txt,'w')
  --for j=1,scores:size(1) do
     --scorce=scores[j][1]
    --file:write(tostring(scorce)..'\n')
  --end
  --file:close()
  --images:add(1):mul(0.5)
  --print(images:size())
  --image.save(fname_png, image.toDisplayTensor(images,4,torch.floor(opt.batchSize/4)))
  --image.save(fname_png, image.toDisplayTensor(images,4,opt.batchSize/1))
  --html = html .. string.format('\n<tr><td>%s</td><td><img src="%s"></td></tr>',
                               --cur_raw_txt, fname_png)
  --os.execute(string.format('echo "%f" > %s', scorces.storage(), fname_txt))
end

--html = html .. '</html>'
--fname_html = string.format('%s.html', opt.dataset)
--os.execute(string.format('echo "%s" > %s', html, fname_html))
