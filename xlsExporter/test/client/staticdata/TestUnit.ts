/*
* Copyright 2017
* This file is automatically generated by python script
* The data is from justForTest.xls
*/

namespace staticdata{
    export class TestUnit{
        //id
        public id:number;
        //字符串
        public name:string;
        //自定义类型（className$type~name;type~name）
        public rewardCertain:Certain[];
        //短整形
        public probability:number;
        //字节型
        public min:number;
        //整型
        public max:number;
        //一维数组
        public single:number[];
        //二维数组
        public double:number[][];

        public constructor(data:any){
            this.id = data.readInt();
            this.name = data.readUTF();
            this.rewardCertain = [];
            for(let i = data.readUnsignedByte()-1; i>=0; --i){
                let child:Certain = new Certain(data);
                this.rewardCertain.push(child);
            }
            this.probability = data.readUnsignedShort();
            this.min = data.readUnsignedByte();
            this.max = data.readInt();
            this.single = [];
            for(let i = data.readUnsignedByte()-1; i>=0; --i){
                this.single.push(data.readInt());
            }
            this.double = [];
            for(let i = data.readUnsignedByte()-1; i>=0; --i){
                let tempList = [];
                this.double.push(tempList);
                for(let j = data.readUnsignedByte()-1; j>=0; --j){
                    tempList.push(data.readUnsignedShort());
                }
            }
        }
    }
}