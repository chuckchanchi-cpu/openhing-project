# Google Form 正确脚本模板 - 供后续开发参考

## ✅ 已验证可用的脚本结构

```javascript
// 30 分鐘車程高效訓練 — 40 題
function createForm() {
  var form = FormApp.create('30 分鐘車程高效訓練');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);

  // 第一部分：中文填充
  form.addPageBreakItem().setTitle('第一部分：中文填充');
  addMC(form, '他＿＿＿＿了一會，才決定摘下那棵麥穗。', ['躊躇','捨棄','錯過','漫長'], '躊躇');
  addMC(form, '聽完老師的解釋，他＿＿＿＿。', ['恍然大悟','語重心長','不約而同','慕名'], '恍然大悟');
  
  // ... 其他题目
  
}

// 辅助函数：添加选择题
function addMC(form, question, options, correctAnswer) {
  var item = form.addMultipleChoiceItem();
  item.setTitle(question);
  item.setRequired(true);
  
  // 添加选项
  for (var i = 0; i < options.length; i++) {
    item.addChoice(options[i]);
  }
  
  // 设置正确答案
  var choices = item.getChoices();
  for (var i = 0; i < choices.length; i++) {
    if (choices[i].getText() === correctAnswer) {
      item.correctResponse(choices[i]);
    }
  }
}
```

---

## 📝 使用要点

1. **创建表单**: `FormApp.create('表单名称')`
2. **设置测验模式**: `form.setIsQuiz(true)`
3. **允许重答**: `form.setShowLinkToRespondAgain(true)`
4. **收集邮箱**: `form.setCollectEmail(false)`（练习用可关闭）
5. **分节**: `form.addPageBreakItem().setTitle('章节名称')`
6. **添加选择题**: 使用 `addMC()` 辅助函数
7. **添加短答题**: 使用 `form.addShortAnswerItem()`

---

## 📁 相关文件位置

- 脚本模板: `~/Desktop/openedujustan/google_form_correct_template.js`
- 指南文档: `~/Desktop/openedujustan/google_form_guidance.md`
- CSV 模板: `~/Desktop/openedujustan/google_form_30min_training.csv`

需要我帮你基于这个模板生成更多科目的练习吗？🦀
