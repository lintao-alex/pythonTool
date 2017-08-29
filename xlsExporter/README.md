#Excel配置导出工具
##同时导出目标语言的解析代码与二进制文件
---
##参看test中的表格，内部定义了一套格式，除基本类型外还有自定义格式的定法
---
##目前只提供了生成TypeScript的功能，要扩展出其它目标语言，只要继承ParseXls，覆写那些必要的方法并写好语言模板
---
###TypeScript中的解压参考如下，其中的"arrayBuffer"为js中的ArrayBuffer对象
###
let compressFile = new Zlib.RawInflate(arrayBuffer)
buffer = compressFile.decompress();
let byteArr = new egret.ByteArray(buffer);
while(byteArr.readAvailable>0) {
	let fileName = byteArr.readUTF();
	let dataType = StaticData[ fileName ];
	let trgMap = StaticData[ 'map' + fileName ]
	let num = byteArr.readUnsignedShort();
	while( num-- > 0 ) {
		let dataObj = new dataType( byteArr );
		trgMap.set( dataObj.id, dataObj )
	}
}