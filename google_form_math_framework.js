# Google Form 成功框架 - 數學小數除法練習

## 📋 表單資訊

- **名稱**: 數學練習：小數除法（一）
- **總題數**: 17 題 MC + 2 個分節 = 19 項
- **作答網址**: https://docs.google.com/forms/d/e/1FAIpQLSfXZNVHVVU4H2NGNriwivdCT_5w4d-0unodRGol16OYw6XJUQ/viewform
- **編輯網址**: https://docs.google.com/forms/d/1ypY9WJl-OMk2WTMcVVoOMmoCH2RhyvQwDBRCHQyGlmI/edit

---

## ✅ 成功腳本代碼

```javascript
// 數學練習：小數除法（一）— 16 題 MC 版（每題附提示）
function createForm() {
  var form = FormApp.create('數學練習：小數除法（一）');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);

  // 第一部分：計算題
  form.addPageBreakItem().setTitle('第一部分：計算題');
  addMC(form, '6.2 ÷ 2 = ?', ['3.1','3.01','31','0.31'], '3.1', '先當整數除：62 ÷ 2 = 31，6.2 有一位小數，答案就係 3.1');
  addMC(form, '8.4 ÷ 6 = ?', ['1.4','14','0.14','1.04'], '1.4', '拆數法：6 ÷ 6 = 1，2.4 ÷ 6 = 0.4');
  addMC(form, '9.3 ÷ 3 = ?', ['3.1','3.3','31','0.31'], '3.1', '拆數法：9 ÷ 3 = 3，0.3 ÷ 3 = 0.1');
  addMC(form, '0.85 ÷ 5 = ?', ['0.17','1.7','0.017','17'], '0.17', '先算 85 ÷ 5 = 17，原數有2位小数 → 0.17');
  addMC(form, '6.48 ÷ 6 = ?', ['1.08','10.8','0.108','108'], '1.08', '先算 648 ÷ 6 = 108，再放2位小数 → 1.08');
  addMC(form, '0.2 ÷ 4 = ?', ['0.05','0.5','5','0.5'], '0.05', '個位不夠除，商寫0加小数點，補0後 20 ÷ 4 = 5');
  addMC(form, '8.1 ÷ 18 = ?', ['0.45','4.5','0.045','45'], '0.45', '先估算 8 ÷ 18 < 1，補0後 81 ÷ 18 = 4.5 → 0.45');
  addMC(form, '50.6 ÷ 22 = ?', ['2.3','23','0.23','2.03'], '2.3', '先算 506 ÷ 22 = 23，再放1位小数 → 2.3');
  addMC(form, '9 ÷ 45 = ?', ['0.2','2','0.02','20'], '0.2', '整数÷整数，商寫0加小数點，補0後 90 ÷ 45 = 2');
  addMC(form, '77 ÷ 14 = ?', ['5.5','55','0.55','5.05'], '5.5', '先算 77 ÷ 14 = 5.5');

  // 第二部分：近似值（取至百分位）
  form.addPageBreakItem().setTitle('第二部分：近似值（取至百分位）');
  addMC(form, '7.21 ÷ 7 ≈ (百分位)', ['1.03','1.30','1.00','1.3'], '1.03', '精確值 1.03，千分位是0 → 不進位');
  addMC(form, '48 ÷ 5 ≈ (百分位)', ['9.60','9.6','9.06','96.0'], '9.60', '精確值 9.6，取至百分位 → 9.60');
  addMC(form, '9.02 ÷ 7 ≈ (百分位)', ['1.29','1.92','1.20','1.9'], '1.29', '精確值 1.288...，千分位是8 → 百分位8進1 → 1.29');
  addMC(form, '75 ÷ 13 ≈ (百分位)', ['5.77','5.70','5.07','5.7'], '5.77', '精確值 5.769...，千分位是9 → 百分位6進1 → 5.77');

  // 第三部分：近似值（取至十分位）
  form.addPageBreakItem().setTitle('第三部分：近似值（取至十分位）');
  addMC(form, '7.21 ÷ 7 ≈ (十分位)', ['1.0','1.3','1.00','1.30'], '1.0', '精確值 1.03，百分位是3 → 十分位0不進位 → 1.0');
  addMC(form, '8.41 ÷ 6 ≈ (十分位)', ['1.4','1.40','1.04','1.00'], '1.4', '精確值 1.401...，百分位是0 → 十分位0不進位 → 1.4');
  addMC(form, '51.2 ÷ 17 ≈ (十分位)', ['3.0','3.01','3.10','3.1'], '3.0', '精確值 3.011...，百分位是1 → 十分位1不進位 → 3.0');
}

// 輔助函數：添加選擇題
function addMC(form, question, options, correctAnswer, hint) {
  var item = form.addMultipleChoiceItem();
  item.setTitle(question + '\n💡 ' + hint);
  item.setRequired(true);
  
  for (var i = 0; i < options.length; i++) {
    item.addChoice(options[i]);
  }
  
  var choices = item.getChoices();
  for (var i = 0; i < choices.length; i++) {
    if (choices[i].getValue() === correctAnswer) {
      item.correctResponse(choices[i]);
    }
  }
  
  item.setFeedbackForCorrectResponse(
    FormApp.createFeedback().setFeedbackText('✅ 正確！')
  );
  item.setFeedbackForIncorrectResponse(
    FormApp.createFeedback().setFeedbackText('❌ 錯誤！正確答案是：' + correctAnswer)
  );
}
```

---

## 🔧 關鍵 API 用法

| 方法 | 用途 | 範例 |
|------|------|------|
| `FormApp.create()` | 創建新表單 | `FormApp.create('表單名稱')` |
| `form.setIsQuiz(true)` | 開啟測驗模式 | `form.setIsQuiz(true)` |
| `form.addPageBreakItem()` | 添加分節 | `form.addPageBreakItem().setTitle('章節名稱')` |
| `form.addMultipleChoiceItem()` | 添加選擇題 | `form.addMultipleChoiceItem()` |
| `item.setTitle()` | 設置題目 | `item.setTitle('題目文字')` |
| `item.addChoice()` | 添加選項 | `item.addChoice('選項文字')` |
| `item.correctResponse()` | 設置正確答案 | `item.correctResponse(choice)` |
| `FormApp.createFeedback()` | 設置反饋 | `FormApp.createFeedback().setFeedbackText('反饋文字')` |

---

## 📝 使用要點

1. **必須包含 `addMC` 輔助函數** - 這是成功關鍵
2. **使用 `var` 而非 `const/let`** - Apps Script 兼容性更好
3. **每題都要調用 `addMC`** - 格式：`addMC(form, 題目, 選項陣列, 正確答案, 提示)`
4. **選項順序不重要** - `correctResponse()` 會自動匹配
5. **提示放在題目文字中** - 使用 `\n💡 ` 換行顯示

---

## 📁 相關文件位置

- 成功框架: `~/Desktop/openedujustan/google_form_math_framework.js`
- CSV 模板: `~/Desktop/openedujustan/google_form_30min_training.csv`
- 指南文檔: `~/Desktop/openedujustan/google_form_guidance.md`
- 數學練習題: `~/Desktop/openedujustan/Maths/Topic_2_DecimalDivision_Practice.md`
