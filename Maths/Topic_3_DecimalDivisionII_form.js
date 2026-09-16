// 數學練習 — 小數除法（二）15分鐘車程版
function createMathForm() {
  var form = FormApp.create('數學：小數除法（二）練習（15分鐘）');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);

  // Section 1: 移小数点法（除數是小數）
  form.addPageBreakItem().setTitle('Section 1: 移小数点法');
  
  addMC(form, '16 ÷ 0.4 = ?', '40', ['40','4','400','0.4'], '💡 技巧-移小数点：把除數變整數，0.4→4，被除數也×10 → 160÷4=40');
  addMC(form, '9 ÷ 0.18 = ?', '50', ['50','5','500','0.5'], '💡 技巧-移小数点：0.18→18（×100），9→900（×100），900÷18=50');
  addMC(form, '0.94 ÷ 0.02 = ?', '47', ['47','4.7','470','0.47'], '💡 技巧-移小数点：0.02→2（×100），0.94→94（×100），94÷2=47');
  addMC(form, '9 ÷ 0.25 = ?', '36', ['36','3.6','360','0.36'], '💡 技巧-移小数点：0.25→25（×100），9→900（×100），900÷25=36');
  addMC(form, '1.7 ÷ 0.05 = ?', '34', ['34','3.4','340','0.34'], '💡 技巧-移小数点：0.05→5（×100），1.7→170（×100），170÷5=34');

  // Section 2: 估算 + 近似值
  form.addPageBreakItem().setTitle('Section 2: 估算 + 近似值');
  
  addMC(form, '10 ÷ 1.8 ≈ ?（取至十分位）', '5.6', ['5.6','5.5','5.0','6.0'], '💡 技巧-估一估：10÷2=5，答案應在5附近；精確計算100÷18=5.55...→5.6');
  addMC(form, '89.5 ÷ 2.7 ≈ ?（取至十分位）', '33.1', ['33.1','30','33.2','30.3'], '💡 技巧-估一估：90÷3=30，答案應在30附近；精確計算895÷27=33.14...→33.1');
  addMC(form, '四捨五入時，百分位是5，十分位應該？', '進位', ['進位','不進','減1','加2'], '💡 技巧-四捨五入：看下一位，≥5進位，<5不進');
  addMC(form, '3.148... 取至十分位是多少？', '3.1', ['3.1','3.2','3.15','3.0'], '💡 技巧-四捨五入：百分位是4（<5）→ 不進位 → 3.1');

  // Section 3: 應用題
  form.addPageBreakItem().setTitle('Section 3: 應用題');
  
  addMC(form, '84.8 cm絲帶做4個蝴蝶結，每個用多少cm？', '21.2', ['21.2','21.2cm','212','2.12'], '💡 技巧-列式：總長÷數量=每份，84.8÷4=21.2cm');
  addMC(form, '松樹高8.6米，木棉樹是它的2.5倍，木棉樹多高？', '21.5米', ['21.5米','2.15米','215米','3.44米'], '💡 技巧-求倍數：用乘法，8.6×2.5=21.5米');
  addMC(form, '松樹高8.6米，是椰子树的2.5倍，椰子树多高？', '3.44米', ['3.44米','34.4米','21.5米','10.85米'], '⚠️ 注意：已知結果求原數用除法，8.6÷2.5=3.44米');
  addMC(form, '做應用題的最後一步應該？', '寫完整答案（含單位）', ['寫完整答案（含單位）','只寫數字','列出算式','估算即可'], '💡 技巧-答題格式：列式→計算→寫完整句子+單位');

  // Section 4: 綜合檢查
  form.addPageBreakItem().setTitle('Section 4: 綜合檢查');
  
  addMC(form, '25.3 ÷ 4.6 = ?', '5.5', ['5.5','55','0.55','5.05'], '💡 技巧-移小数点：4.6→46（×10），25.3→253（×10），253÷46=5.5');
  addMC(form, '10.8 ÷ 2.4 = ?', '4.5', ['4.5','45','0.45','450'], '💡 技巧-移小数点：2.4→24（×10），10.8→108（×10），108÷24=4.5');
  addMC(form, '2.28 ÷ 1.6 = ?', '1.425', ['1.425','14.25','0.1425','142.5'], '💡 技巧-補0規律：1.6→16（×10），2.28→22.8（×10），22.8÷16=1.425');
  addMC(form, '估算 10 ÷ 1.8 時，最接近的整數估算式是？', '10 ÷ 2 = 5', ['10 ÷ 2 = 5','10 ÷ 1 = 10','20 ÷ 2 = 10','10 ÷ 3 = 3.3'], '💡 技巧-估一估：1.8接近2，所以用10÷2=5作估算');
}

// 輔助函數：添加選擇題
function addMC(form, question, correctAnswer, options, hint) {
  var item = form.addMultipleChoiceItem();
  item.setTitle(question + '\n' + hint);
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
    FormApp.createFeedback().setFeedbackText('✅ Correct!')
  );
  item.setFeedbackForIncorrectResponse(
    FormApp.createFeedback().setFeedbackText('❌ Wrong! The answer is: ' + correctAnswer)
  );
}
