#target illustrator
// ==============================================================================
// 🖨️ SIWASUP BANNER GENERATOR - EXTENDSCRIPT FOR ADOBE ILLUSTRATOR
// File: siwasup_banner_generator.jsx
// Compatible with: Adobe Illustrator CC 2019 - 2025 (Win/Mac)
// Direct Layer Binding:
//   - Ticker_NumberA: Phone Number 1
//   - Ticker_NumberB: Phone Number 2
//   - Ticker_AgentInfo: Agent details (e.g. 'ติดต่อ: คุณเอ (ตัวแทนพื้นที่โซนบางนา) LINE ID: ของตัวแทน')
//   - Job_Discription: Web/LINE tagline ('www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี @siwasup')
//   - Horsale: Red Header block + 'ขายด่วน'
//   - Footer_Company: Siwasup Logo + Company Service + QR Code
// ==============================================================================

(function() {
    if (app.documents.length === 0) {
        alert('กรุณาเปิดไฟล์เทมเพลต Ads200x160.ait ก่อนรันสคริปต์นี้ครับ', 'Siwasup Banner Tool');
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

    // Helper: Find textFrame by layer name or text frame name
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

    // Locate Target Layers
    var tfPhoneA = findTargetTextFrame(doc, 'Ticker_NumberA');
    var tfPhoneB = findTargetTextFrame(doc, 'Ticker_NumberB');
    var tfAgentInfo = findTargetTextFrame(doc, 'Ticker_AgentInfo');
    var tfJobDisc = findTargetTextFrame(doc, 'Job_Discription');

    // Defaults
    var curPhoneA = tfPhoneA ? tfPhoneA.contents : '094-462-9796';
    var curPhoneB = tfPhoneB ? tfPhoneB.contents : '096-129-2459';
    var curAgentInfo = tfAgentInfo ? tfAgentInfo.contents : 'ติดต่อ: คุณเอ (ตัวแทนพื้นที่โซนบางนา) LINE ID: ของตัวแทน';
    var curJobDisc = tfJobDisc ? tfJobDisc.contents : 'www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี  @siwasup';

    // ScriptUI Dialog
    var dlg = new Window('dialog', 'Siwasup Vinyl Banner Generator (Ads200x160)');
    dlg.orientation = 'column';
    dlg.alignChildren = ['fill', 'top'];
    dlg.spacing = 10;
    dlg.margins = 16;

    // Header Panel
    var pnlHeader = dlg.add('panel', undefined, '🏢 บริษัท ศิวาทรัพย์ แอสเซท จำกัด (Ads200x160.ait)');
    pnlHeader.orientation = 'column';
    pnlHeader.alignChildren = ['left', 'top'];
    var lblInfo = pnlHeader.add('statictext', undefined, 'ไฟล์ปัจจุบัน: ' + doc.name);
    lblInfo.graphics.foregroundColor = lblInfo.graphics.newPen(dlg.graphics.PenType.SOLID_COLOR, [0.1, 0.4, 0.7, 1], 1);

    // Inputs Panel
    var pnlInputs = dlg.add('panel', undefined, '📞 ข้อมูลป้ายไวนิล (Direct Layer Binding)');
    pnlInputs.orientation = 'column';
    pnlInputs.alignChildren = ['fill', 'top'];
    pnlInputs.spacing = 8;

    // Phone A
    var grpA = pnlInputs.add('group');
    grpA.orientation = 'row';
    var lblA = grpA.add('statictext', undefined, 'เบอร์โทร 1 (Ticker_NumberA):');
    lblA.preferredSize.width = 190;
    var txtPhoneA = grpA.add('edittext', undefined, curPhoneA);
    txtPhoneA.preferredSize.width = 220;

    // Phone B
    var grpB = pnlInputs.add('group');
    grpB.orientation = 'row';
    var lblB = grpB.add('statictext', undefined, 'เบอร์โทร 2 (Ticker_NumberB):');
    lblB.preferredSize.width = 190;
    var txtPhoneB = grpB.add('edittext', undefined, curPhoneB);
    txtPhoneB.preferredSize.width = 220;

    // Ticker_AgentInfo
    var grpInfo = pnlInputs.add('group');
    grpInfo.orientation = 'row';
    var lblInfoTxt = grpInfo.add('statictext', undefined, 'ข้อมูลตัวแทน (Ticker_AgentInfo):');
    lblInfoTxt.preferredSize.width = 190;
    var txtAgentInfo = grpInfo.add('edittext', undefined, curAgentInfo);
    txtAgentInfo.preferredSize.width = 300;

    // Job_Discription
    var grpJob = pnlInputs.add('group');
    grpJob.orientation = 'row';
    var lblJob = grpJob.add('statictext', undefined, 'แถบเว็บ/ไลน์ (Job_Discription):');
    lblJob.preferredSize.width = 190;
    var txtJobDisc = grpJob.add('edittext', undefined, curJobDisc);
    txtJobDisc.preferredSize.width = 300;

    // Presets
    var grpPreset = pnlInputs.add('group');
    grpPreset.orientation = 'row';
    var lblPreset = grpPreset.add('statictext', undefined, 'โหลดด่วนจากรหัสตัวแทน:');
    lblPreset.preferredSize.width = 190;
    var dropAgent = grpPreset.add('dropdownlist', undefined, [
        '-- เลือกตัวแทนศิวศุภ --',
        'S02 - บัว (ส่วนกลาง: 094-462-9796 / 096-129-2459)',
        'S22 - บัวรา / เจี๊ยบ (06-2396-5161)',
        'S05 - ต้น ชาญชัย (081-811-6677)'
    ]);
    dropAgent.selection = 0;
    dropAgent.onChange = function() {
        if (dropAgent.selection.index === 1) {
            txtPhoneA.text = '094-462-9796';
            txtPhoneB.text = '096-129-2459';
            txtAgentInfo.text = 'ติดต่อ: แอดมินบัว (ส่วนกลาง) LINE: @siwasup';
        } else if (dropAgent.selection.index === 2) {
            txtPhoneA.text = '06-2396-5161';
            txtPhoneB.text = '096-129-2459';
            txtAgentInfo.text = 'ติดต่อ: บัวรา (S22) LINE: @siwasup';
        }
    };

    // Action Buttons
    var grpBtns = dlg.add('group');
    grpBtns.orientation = 'row';
    grpBtns.alignment = ['center', 'bottom'];
    grpBtns.spacing = 10;

    var btnApply = grpBtns.add('button', undefined, '⚡ อัปเดตลงบนจอทันที (Live Apply)');
    var btnExportPDF = grpBtns.add('button', undefined, '💾 ส่งออก PDF 1:1');
    var btnCancel = grpBtns.add('button', undefined, 'ปิด', { name: 'cancel' });

    function applyChanges() {
        var count = 0;
        if (tfPhoneA) { tfPhoneA.contents = txtPhoneA.text; count++; }
        if (tfPhoneB) { tfPhoneB.contents = txtPhoneB.text; count++; }
        if (tfAgentInfo) { tfAgentInfo.contents = txtAgentInfo.text; count++; }
        if (tfJobDisc) { tfJobDisc.contents = txtJobDisc.text; count++; }
        app.redraw();
        return count;
    }

    btnApply.onClick = function() {
        var cnt = applyChanges();
        alert('อัปเดตข้อมูลสำเร็จ (' + cnt + ' จุด)!\\nเลเยอร์ Ticker_NumberA/B และ Ticker_AgentInfo ถูกปรับเรียบร้อยแล้วครับ', 'Siwasup Banner Tool');
        dlg.close();
    };

    btnExportPDF.onClick = function() {
        applyChanges();
        var saveFile = File.saveDialog('เลือกที่บันทึกไฟล์ PDF สำหรับพิมพ์ไวนิล 1:1 (200x160 cm)', 'PDF Files:*.pdf');
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
