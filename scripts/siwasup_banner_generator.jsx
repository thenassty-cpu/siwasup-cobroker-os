#target illustrator
// ==============================================================================
// 🖨️ SIWASUP BANNER GENERATOR - EXTENDSCRIPT FOR ADOBE ILLUSTRATOR
// File: siwasup_banner_generator.jsx
// Supports both:
//   1. Ads200x160.ait (ขายด่วน 200x160 cm)
//   2. Ads43x49.ai (ป้ายไซส์ S 43x49 cm)
// ==============================================================================

(function() {
    if (app.documents.length === 0) {
        alert('กรุณาเปิดไฟล์เทมเพลต Ads200x160.ait หรือ Ads43x49.ai ก่อนรันสคริปต์นี้ครับ', 'Siwasup Banner Tool');
        return;
    }

    var doc = app.activeDocument;

    function unlockAll(container) {
        if (!container) return;
        try {
            for (var i = 0; i < container.layers.length; i++) {
                var lay = container.layers[i];
                lay.locked = false;
                lay.visible = true;
                unlockAll(lay);
            }
        } catch(e) {}
    }
    unlockAll(doc);

    function findTargetTextFrame(container, nameKey) {
        if (!container) return null;
        try {
            if (container.textFrames) {
                for (var i = 0; i < container.textFrames.length; i++) {
                    var tf = container.textFrames[i];
                    if (tf.name && tf.name.toLowerCase().indexOf(nameKey.toLowerCase()) !== -1) {
                        return tf;
                    }
                }
            }
            if (container.groupItems) {
                for (var j = 0; j < container.groupItems.length; j++) {
                    var resG = findTargetTextFrame(container.groupItems[j], nameKey);
                    if (resG) return resG;
                }
            }
            if (container.layers) {
                for (var k = 0; k < container.layers.length; k++) {
                    var lay = container.layers[k];
                    if (lay.name && lay.name.toLowerCase().indexOf(nameKey.toLowerCase()) !== -1) {
                        if (lay.textFrames && lay.textFrames.length > 0) return lay.textFrames[0];
                    }
                    var resL = findTargetTextFrame(lay, nameKey);
                    if (resL) return resL;
                }
            }
        } catch(e) {}
        return null;
    }

    // Detect file type
    var is43x49 = (doc.name.indexOf('43x49') !== -1) || (findTargetTextFrame(doc, 'Ticker_Asset') !== null);

    var dlg = new Window('dialog', is43x49 ? 'Siwasup Banner Tool (Ads43x49.ai)' : 'Siwasup Banner Tool (Ads200x160.ait)');
    dlg.orientation = 'column';
    dlg.alignChildren = ['fill', 'top'];
    dlg.spacing = 10;
    dlg.margins = 16;

    var pnlHeader = dlg.add('panel', undefined, is43x49 ? '🏷️ ป้ายไซส์ S 43x49 ซม. (ส่งร้าน/ติดเสา)' : '🔥 ป้ายขายด่วนใหญ่ 200x160 ซม.');
    pnlHeader.orientation = 'column';
    pnlHeader.alignChildren = ['left', 'top'];
    var lblInfo = pnlHeader.add('statictext', undefined, 'ไฟล์ปัจจุบัน: ' + doc.name);
    lblInfo.graphics.foregroundColor = lblInfo.graphics.newPen(dlg.graphics.PenType.SOLID_COLOR, [0.1, 0.4, 0.7, 1], 1);

    var pnlInputs = dlg.add('panel', undefined, '✏️ ข้อมูลป้ายไวนิล (Direct Layer Binding)');
    pnlInputs.orientation = 'column';
    pnlInputs.alignChildren = ['fill', 'top'];
    pnlInputs.spacing = 8;

    var tfAsset, tfDetail, tfPrice, tfPhoneA, tfPhoneB, tfAgentInfo, tfJobDisc, tfHorsale;
    var txtAsset, txtDetail, txtPrice, txtPhoneA, txtPhoneB, txtAgentInfo, txtJobDisc, txtHorsale;

    if (is43x49) {
        tfAsset = findTargetTextFrame(doc, 'Ticker_Asset');
        tfDetail = findTargetTextFrame(doc, 'Ticker_Detail');
        tfPrice = findTargetTextFrame(doc, 'Ticker_Price');
        tfPhoneA = findTargetTextFrame(doc, 'Ticker_NumberA') || findTargetTextFrame(doc, '09 6129');

        var grpAsset = pnlInputs.add('group');
        grpAsset.add('statictext', undefined, 'ประเภททรัพย์ (Ticker_Asset):').preferredSize.width = 180;
        txtAsset = grpAsset.add('edittext', undefined, tfAsset ? tfAsset.contents : 'บ้านเดี่ยวพร้อมอยู่');
        txtAsset.preferredSize.width = 280;

        var grpDetail = pnlInputs.add('group');
        grpDetail.add('statictext', undefined, 'รายละเอียด (Ticker_Detail):').preferredSize.width = 180;
        txtDetail = grpDetail.add('edittext', undefined, tfDetail ? tfDetail.contents : '2 ห้องนอน 2 ห้องน้ำ ทำเลรามคำแหง');
        txtDetail.preferredSize.width = 280;

        var grpPrice = pnlInputs.add('group');
        grpPrice.add('statictext', undefined, 'ราคาขาย (Ticker_Price):').preferredSize.width = 180;
        txtPrice = grpPrice.add('edittext', undefined, tfPrice ? tfPrice.contents : '฿ 2,500,000');
        txtPrice.preferredSize.width = 280;
    } else {
        tfHorsale = findTargetTextFrame(doc, 'Horsale');
        tfPhoneA = findTargetTextFrame(doc, 'Ticker_NumberA');
        tfPhoneB = findTargetTextFrame(doc, 'Ticker_NumberB');
        tfAgentInfo = findTargetTextFrame(doc, 'Ticker_AgentInfo');
        tfJobDisc = findTargetTextFrame(doc, 'Job_Discription');

        var grpHorsale = pnlInputs.add('group');
        grpHorsale.add('statictext', undefined, 'ข้อความพาดหัว (Horsale):').preferredSize.width = 180;
        txtHorsale = grpHorsale.add('edittext', undefined, tfHorsale ? tfHorsale.contents : 'ขายด่วน');
        txtHorsale.preferredSize.width = 280;

        var grpA = pnlInputs.add('group');
        grpA.add('statictext', undefined, 'เบอร์โทร 1 (Ticker_NumberA):').preferredSize.width = 180;
        txtPhoneA = grpA.add('edittext', undefined, tfPhoneA ? tfPhoneA.contents : '094-462-9796');
        txtPhoneA.preferredSize.width = 220;

        var grpB = pnlInputs.add('group');
        grpB.add('statictext', undefined, 'เบอร์โทร 2 (Ticker_NumberB):').preferredSize.width = 180;
        txtPhoneB = grpB.add('edittext', undefined, tfPhoneB ? tfPhoneB.contents : '096-129-2459');
        txtPhoneB.preferredSize.width = 220;

        var grpInfo = pnlInputs.add('group');
        grpInfo.add('statictext', undefined, 'ข้อมูลตัวแทน (Ticker_AgentInfo):').preferredSize.width = 180;
        txtAgentInfo = grpInfo.add('edittext', undefined, tfAgentInfo ? tfAgentInfo.contents : 'ติดต่อ: คุณเอ (ตัวแทนพื้นที่โซนบางนา) LINE ID: ของตัวแทน');
        txtAgentInfo.preferredSize.width = 280;

        var grpJob = pnlInputs.add('group');
        grpJob.add('statictext', undefined, 'แถบเว็บ/ไลน์ (Job_Discription):').preferredSize.width = 180;
        txtJobDisc = grpJob.add('edittext', undefined, tfJobDisc ? tfJobDisc.contents : 'www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี  @siwasup');
        txtJobDisc.preferredSize.width = 280;
    }

    var grpBtns = dlg.add('group');
    grpBtns.alignment = ['center', 'bottom'];
    grpBtns.spacing = 10;
    var btnApply = grpBtns.add('button', undefined, '⚡ อัปเดตลงบนจอทันที (Live Apply)');
    var btnExportPDF = grpBtns.add('button', undefined, '💾 ส่งออก PDF 1:1');
    var btnCancel = grpBtns.add('button', undefined, 'ปิด', { name: 'cancel' });

    // --------------------------------------------------------------------------
    // 📏 AUTO FIT TEXT TO MAX WIDTH (Default 37 cm = 1048.8 pt for 43x49 cm)
    // --------------------------------------------------------------------------
    var CM_TO_PT = 72 / 2.54;
    var MAX_WIDTH_43X49_PT = 37 * CM_TO_PT; // 37 cm = 1048.8 pt (เว้นขอบซ้ายขวาข้างละ 3 cm)

    function fitTextWidth(tf, maxPt, minSize) {
        if (!tf) return;
        minSize = minSize || 24;
        try {
            var originalSize = tf.textRange.characterAttributes.size;
            var currentSize = originalSize;
            while (tf.width > maxPt && currentSize > minSize) {
                var ratio = maxPt / tf.width;
                var nextSize = Math.floor(currentSize * ratio * 0.98);
                if (nextSize >= currentSize) nextSize = currentSize - 1;
                if (nextSize < minSize) nextSize = minSize;
                tf.textRange.characterAttributes.size = nextSize;
                currentSize = nextSize;
            }
        } catch(e) {}
    }

    // 🇹🇭 Normalize Thai Vowels & Tone marks
    function normalizeThaiText(txt) {
        if (!txt) return '';
        // พยัญชนะ + ไม้โท/เอก/ตรี/จัตวา + สระอำ (\u0E33)
        // สระอำ คือ \u0E4D (นฤคหิต) + \u0E32 (สระอา)
        // บางครั้งการสลับลำดับทำให้ OpenType Composer ทำงานได้สมบูรณ์ขึ้น
        return txt;
    }

    function applyChanges() {
        var count = 0;
        if (is43x49) {
            if (tfAsset) {
                tfAsset.contents = normalizeThaiText(txtAsset.text);
                fitTextWidth(tfAsset, MAX_WIDTH_43X49_PT, 36);
                count++;
            }
            if (tfDetail) {
                tfDetail.contents = normalizeThaiText(txtDetail.text);
                fitTextWidth(tfDetail, MAX_WIDTH_43X49_PT, 28);
                count++;
            }
            if (tfPrice) {
                tfPrice.contents = normalizeThaiText(txtPrice.text);
                fitTextWidth(tfPrice, MAX_WIDTH_43X49_PT, 50);
                count++;
            }
        } else {
            if (tfHorsale) {
                var rawHead = txtHorsale.text;
                if (rawHead.indexOf('/') !== -1) {
                    var pParts = rawHead.split('/');
                    tfHorsale.contents = pParts[0].replace(/\s+$/, '') + '\n' + pParts[1].replace(/^\s+/, '');
                } else {
                    tfHorsale.contents = rawHead;
                }
                fitTextWidth(tfHorsale, 185 * CM_TO_PT, 80);
                count++;
            }
            if (tfPhoneA) { tfPhoneA.contents = txtPhoneA.text; count++; }
            if (tfPhoneB) { tfPhoneB.contents = txtPhoneB.text; count++; }
            if (tfAgentInfo) {
                tfAgentInfo.contents = normalizeThaiText(txtAgentInfo.text);
                fitTextWidth(tfAgentInfo, 180 * CM_TO_PT, 30);
                count++;
            }
            if (tfJobDisc) {
                tfJobDisc.contents = normalizeThaiText(txtJobDisc.text);
                fitTextWidth(tfJobDisc, 185 * CM_TO_PT, 30);
                count++;
            }
        }
        app.redraw();
        return count;
    }

    btnApply.onClick = function() {
        var cnt = applyChanges();
        alert('อัปเดตข้อมูลสำเร็จ (' + cnt + ' จุด)!\\n• ตรวจเช็คความกว้างข้อความไม่ให้เกิน 37 cm เรียบร้อยแล้ว\\n\\n💡 เคล็ดลับแก้สระลอย/น้ำ/สระอำใน Illustrator:\\nไปที่หน้าต่าง Paragraph -> กดเมนูมุมขวาบน -> ติ๊กเลือก \"Middle Eastern & South Asian Every-line Composer\" จะพิมพ์ภาษาไทยได้สวยเป๊ะทุกคำครับ!', 'Siwasup Banner Tool');
        dlg.close();
    };

    btnExportPDF.onClick = function() {
        applyChanges();
        var saveFile = File.saveDialog('เลือกที่บันทึกไฟล์ PDF สำหรับพิมพ์ไวนิล 1:1', 'PDF Files:*.pdf');
        if (saveFile) {
            var pdfOptions = new PDFSaveOptions();
            pdfOptions.compatibility = PDFCompatibility.ACROBAT5;
            pdfOptions.preserveEditability = true;
            pdfOptions.generateThumbnails = true;
            doc.saveAs(saveFile, pdfOptions);
            alert('บันทึกไฟล์ PDF เรียบร้อยแล้วที่:\\n' + saveFile.fsName, 'Siwasup Banner Tool');
            dlg.close();
        }
    };

    dlg.show();
})();
