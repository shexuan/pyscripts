（1）先将此模块添加到环境变量搜索路径中.
	import sys
	sys.path.append("/path/to/file")

（2）导入模块与其他模块用法类似.如在ipython3中：
	>>> import plot_barcode
	>>> s=Barcode('ACGTGA')  #建立一个Barcode类对象
	>>> s.plot_barcode()  #调用plot_barcode方法绘图
