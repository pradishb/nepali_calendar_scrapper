import xml.etree.cElementTree as ET
import xml.etree.ElementTree as etree
from copy import copy

def write(dashi,eday,nday,fest,holiday,months):
    root = ET.Element("Root")

    for month in months:
        dashi[month].reverse()
        eday[month].reverse()
        nday[month].reverse()
        fest[month].reverse()

        nepali_days = [
            ("आईत\nSun", "normal"),
            ("सोम\nMon", "normal"),
            ("मंगल\nTue", "normal"),
            ("बुध\nWed", "normal"),
            ("बिही\nThu", "normal"),
            ("शुक्र\nFri", "normal"),
            ("शनि\nSat", "holiday"),]

        aid =  'http://ns.adobe.com/AdobeInDesign/4.0/'
        aid5 =  'http://ns.adobe.com/AdobeInDesign/5.0/'
        ns = {"xmlns:aid": aid, "xmlns:aid5": aid5}
        for attr, uri in ns.items():
            etree.register_namespace(attr.split(":")[1], uri)

        
        table = ET.SubElement(root, "Table", {
            etree.QName(aid, "table"):"table",
            etree.QName(aid, "trows"):"16",
            etree.QName(aid, "tcols"):"14",
            etree.QName(aid5, "tablestyle"):"month",
            })

        # headers
        for d in nepali_days:
            ET.SubElement(table, "Cell", {
                etree.QName(aid, "table"):"cell",
                etree.QName(aid, "crows"):"1",
                etree.QName(aid, "ccols"):"2",
                etree.QName(aid5, "cellstyle"):"nheader",
                etree.QName(aid, "cstyle"):d[1],
                }).text = d[0]
        
        # fest
        for j in range(5):
            i = 0
            for _ in range(7):
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"3",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid, "ccolwidth"):"10",
                    etree.QName(aid5, "cellstyle"):"fest",
                    etree.QName(aid, "cstyle"):holiday[month][7*j + i],
                    }).text = fest[month].pop()
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"1",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid, "ccolwidth"):"42",
                    etree.QName(aid5, "cellstyle"):"dashi",
                    etree.QName(aid, "cstyle"):holiday[month][7*j + i],
                    }).text = dashi[month].pop()
                i += 1
            i = 0
            for _ in range(7):
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"1",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid, "ccolwidth"):"42",
                    etree.QName(aid5, "cellstyle"):"nday",
                    etree.QName(aid, "cstyle"):holiday[month][7*j + i],
                    }).text = nday[month].pop()
                i += 1
            i = 0
            for _ in range(7):
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"1",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid, "ccolwidth"):"42",
                    etree.QName(aid5, "cellstyle"):"eday",
                    etree.QName(aid, "cstyle"):holiday[month][7*j + i],
                    }).text = eday[month].pop()
                i += 1

    


    tree = ET.ElementTree(root)
    tree.write("output.xml",  encoding='UTF-8', xml_declaration=True)
