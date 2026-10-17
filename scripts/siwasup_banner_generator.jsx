#target illustrator
// ==============================================================================
// 🖨️ SIWASUP BANNER GENERATOR - EXTENDSCRIPT FOR ADOBE ILLUSTRATOR
// File: siwasup_banner_generator.jsx
// Compatible with: Adobe Illustrator CC 2019 - 2025 (Win/Mac)
// Supports sizes: 200x160 cm, 43x49 cm, and custom vinyl banners
// Direct Layer Binding: Ticker_NumberA, Ticker_NumberB, Ticker_Subtitle
// ==============================================================================

(function() {
    if (app.documents.length === 0) {
        alert('กรุณาเปิดไฟล์เทมเพลตป้าย (.ai / .ait) ก่อนรันสคริปต์นี้ครับ', 'Siwasup Banner Tool');
        return;
    }

    var doc = app.activeDocument;

    // Helper: Unlock all layers recursively
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

    // Helper: Find textFrame by name or content substring
    function findTargetTextFrame(container, nameKey, contentKey) {
        if (!container) return null;
        try {
            // 1. Search textFrames in this container
            if (container.textFrames) {
                for (var i = 0; i < container.textFrames.length; i++) {
                    var tf = container.textFrames[i];
                    if (nameKey && tf.name && tf.name.toLowerCase().indexOf(nameKey.toLowerCase()) !== -1) {
                        return tf;
                    }
                    if (contentKey && tf.contents && tf.contents.indexOf(contentKey) !== -1) {
                        return tf;
                    }
                }
            }

            // 2. Search groupItems
            if (container.groupItems) {
                for (var j = 0; j < container.groupItems.length; j++) {
                    var resG = findTargetTextFrame(container.groupItems[j], nameKey, contentKey);
                    if (resG) return resG;
                }
            }

            // 3. Search child layers
            if (container.layers) {
                for (var k = 0; k < container.layers.length; k++) {
                    var resL = findTargetTextFrame(container.layers[k], nameKey, contentKey);
                    if (resL) return resL;
                }
            }
        } catch(e) {}
        return null;
    }

    // Locate Key Layers / Frames
    var tfPhoneA = findTargetTextFrame(doc, 'Ticker_NumberA', null);
    var tfPhoneB = findTargetTextFrame(doc, 'Ticker_NumberB', null);
    var tfSubtitle = findTargetTextFrame(doc, null, 'All About Assets');
    if (!tfSubtitle) tfSubtitle = findTargetTextFrame(doc, 'Ticker_Subtitle', null);

    // Default values from current doc or standard
    var curPhoneA = tfPhoneA ? tfPhoneA.contents : '094-462-9796';
    var curPhoneB = tfPhoneB ? tfPhoneB.contents : '096-129-2459';
    var curSubtitle = tfSubtitle ? tfSubtitle.contents.replace('All About Assets', 'Siwasup Asset') : 'เพจ: ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี by Siwasup Asset';

    // Build ScriptUI Dialog
    var dlg = new Window('dialog', 'Siwasup Vinyl Banner Generator (ระบบปรับเบอร์ป้ายไวนิล)');
    dlg.orientation = 'column';
    dlg.alignChildren = ['fill', 'top'];
    dlg.spacing = 10;
    dlg.margins = 16;

    // Header Panel
    var pnlHeader = dlg.add('panel', undefined, '🏢 บริษัท ศิวาทรัพย์ แอสเซท จำกัด');
    pnlHeader.orientation = 'column';
    pnlHeader.alignChildren = ['left', 'top'];
    var lblInfo = pnlHeader.add('statictext', undefined, 'เอกสารปัจจุบัน: ' + doc.name);
    lblInfo.graphics.foregroundColor = lblInfo.graphics.newPen(dlg.graphics.PenType.SOLID_COLOR, [0.1, 0.4, 0.7, 1], 1);

    // Inputs Panel
    var pnlInputs = dlg.add('panel', undefined, '📞 ข้อมูลเบอร์โทรและข้อความป้าย');
    pnlInputs.orientation = 'column';
    pnlInputs.alignChildren = ['fill', 'top'];
    pnlInputs.spacing = 8;

    // Phone A
    var grpA = pnlInputs.add('group');
    grpA.orientation = 'row';
    var lblA = grpA.add('statictext', undefined, 'เบอร์โทร 1 (Ticker_NumberA):');
    lblA.preferredSize.width = 180;
    var txtPhoneA = grpA.add('edittext', undefined, curPhoneA);
    txtPhoneA.preferredSize.width = 200;

    // Phone B
    var grpB = pnlInputs.add('group');
    grpB.orientation = 'row';
    var lblB = grpB.add('statictext', undefined, 'เบอร์โทร 2 (Ticker_NumberB):');
    lblB.preferredSize.width = 180;
    var txtPhoneB = grpB.add('edittext', undefined, curPhoneB);
    txtPhoneB.preferredSize.width = 200;

    // Subtitle / Page text (Replaces All About Assets)
    var grpSub = pnlInputs.add('group');
    grpSub.orientation = 'row';
    var lblSub = grpSub.add('statictext', undefined, 'ข้อความเพจ / สโลแกน:');
    lblSub.preferredSize.width = 180;
    var txtSubtitle = grpSub.add('edittext', undefined, curSubtitle);
    txtSubtitle.preferredSize.width = 260;

    // Quick Agent Preset selector
    var grpPreset = pnlInputs.add('group');
    grpPreset.orientation = 'row';
    var lblPreset = grpPreset.add('statictext', undefined, 'โหลดด่วนจากรหัสตัวแทน:');
    lblPreset.preferredSize.width = 180;
    var dropAgent = grpPreset.add('dropdownlist', undefined, [
        '-- เลือกตัวแทนศิวศุภ --',
        'S02 - บัว (ส่วนกลาง: 094-462-9796 / 096-129-2459)',
        'S22 - เจี๊ยบ / บัวรา (06-2396-5161)',
        'S05 - ต้น ชาญชัย (081-811-6677)',
        'S12 - เอกชัย (089-123-4567)'
    ]);
    dropAgent.selection = 0;
    dropAgent.onChange = function() {
        if (dropAgent.selection.index === 1) {
            txtPhoneA.text = '094-462-9796';
            txtPhoneB.text = '096-129-2459';
            txtSubtitle.text = 'เพจ: ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี by Siwasup Asset';
        } else if (dropAgent.selection.index === 2) {
            txtPhoneA.text = '06-2396-5161';
            txtPhoneB.text = '096-129-2459';
            txtSubtitle.text = 'ตัวแทน: บัวรา (S22) • Siwasup Asset';
        }
    };

    // Buttons
    var grpBtns = dlg.add('group');
    grpBtns.orientation = 'row';
    grpBtns.alignment = ['center', 'bottom'];
    grpBtns.spacing = 10;

    var btnApply = grpBtns.add('button', undefined, '⚡ อัปเดตลงบนจอทันที (Live Apply)');
    var btnExportPDF = grpBtns.add('button', undefined, '💾 ส่งออก PDF 1:1');
    var btnCancel = grpBtns.add('button', undefined, 'ยกเลิก', { name: 'cancel' });

    // Function: Apply texts to active document
    function applyChanges() {
        var updated = 0;
        if (tfPhoneA) {
            tfPhoneA.contents = txtPhoneA.text;
            updated++;
        }
        if (tfPhoneB) {
            tfPhoneB.contents = txtPhoneB.text;
            updated++;
        }
        if (tfSubtitle) {
            tfSubtitle.contents = txtSubtitle.text;
            updated++;
        } else {
            // Try to find any text with All About Assets again
            var anyAllAbout = findTargetTextFrame(doc, null, 'All About Assets');
            if (anyAllAbout) {
                anyAllAbout.contents = txtSubtitle.text;
                updated++;
            }
        }
        app.redraw();
        return updated;
    }

    btnApply.onClick = function() {
        var cnt = applyChanges();
        alert('อัปเดตข้อความสำเร็จ (' + cnt + ' จุด)!\\nเบอร์โทรและข้อความถูกปรับเปลี่ยนเรียบร้อยแล้วครับ', 'Siwasup Banner Tool');
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
