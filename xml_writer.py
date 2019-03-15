import xml.etree.cElementTree as ET
import xml.etree.ElementTree as etree

def write(dashi,eday,nday,fest,months):
    root = ET.Element("Root")

    for month in months:
        dashi[month].reverse()
        eday[month].reverse()
        nday[month].reverse()
        fest[month].reverse()

        nepali_days = [
            "आईत\nSun",
            "सोम\nMon",
            "मंगल\nTue",
            "बुध\nWed",
            "बिही\nThu",
            "शुक्र\nFri",
            "शनि\nSat"]

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
                }).text = d
        
        # fest
        for _ in range(5):
            for _ in range(7):
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"3",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid, "ccolwidth"):"10",
                    etree.QName(aid5, "cellstyle"):"fest",
                    }).text = fest[month].pop()
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"1",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid5, "cellstyle"):"dashi",
                    }).text = dashi[month].pop()
            for _ in range(7):
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"1",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid5, "cellstyle"):"nday",
                    }).text = nday[month].pop()
            for _ in range(7):
                ET.SubElement(table, "Cell", {
                    etree.QName(aid, "table"):"cell",
                    etree.QName(aid, "crows"):"1",
                    etree.QName(aid, "ccols"):"1",
                    etree.QName(aid5, "cellstyle"):"eday",
                    }).text = eday[month].pop()

    


    tree = ET.ElementTree(root)
    tree.write("filename.xml",  encoding='UTF-8', xml_declaration=True)
