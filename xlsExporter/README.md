#Excel���õ�������
##ͬʱ����Ŀ�����ԵĽ���������������ļ�
---
##�ο�test�еı���ڲ�������һ�׸�ʽ�������������⻹���Զ����ʽ�Ķ���
---
##Ŀǰֻ�ṩ������TypeScript�Ĺ��ܣ�Ҫ��չ������Ŀ�����ԣ�ֻҪ�̳�ParseXls����д��Щ��Ҫ�ķ�����д������ģ��
---
###TypeScript�еĽ�ѹ�ο����£����е�"arrayBuffer"Ϊjs�е�ArrayBuffer����
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