# coding: utf-8
"""
使用说明：
1. 安装tesseract。参考：https://github.com/tesseract-ocr/tesseract
2. 安装中文语言包并放在对应位置：https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.chi_sim.tar.gz
"""
import os
import traceback

def  processImages(path, save):
	cmdtpl = 'tesseract {} {} -l chi_sim'

	imgList = os.listdir(path)
	os.chdir(path)
	for i in range(1, len(imgList)):
		cmd = ""
		try:
			result = '%s/result-%s' % (save, imgList[i].split('.')[0])
			cmd = cmdtpl.format(imgList[i], result)
			os.popen(cmd)
			cleanResult(result+'.txt')
		except Exception as e:
			print "process ", cmd, "error: ", traceback.format_exc()
		else:
			print "process ", imgList[i], "successfully."

transfers = {
	'o ': '。',
	'o': '。',
	'\n': '',
	'， ': '，',
	':': '：',
	': ': '：',
	'。 ': '。',
	',': '，',
	', ': '，',
}
def cleanResult(path):
	result = ""
	with open(path) as f:
		result = f.read()

	for k, v in transfers.items():
		result = result.replace(k, v)
	with open(path, "w") as f:
		f.write(result)

if __name__ == '__main__':
	path = "/Users/elexu/Pictures/OCR"
	save = "/Users/elexu/Pictures/OCR_result"
	processImages(path, save)
		