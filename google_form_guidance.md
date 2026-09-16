# Google Form 设置指南 - 30分钟车程高效训练

## 📋 表单信息

- **名称**: 30分钟车程高效训练
- **总题目数**: 44题
- **分节结构**: 4个section（中文填充、中文语法、英文语法、常识生物分类）
- **作答网址**: https://docs.google.com/forms/d/e/1FAIpQLSfa58z_6o367Xqh_rYNV9055mNhNDWeY17HwYrpnFVnZEbZvA/viewform
- **编辑网址**: https://docs.google.com/forms/d/1azCWUft4hCs7FNIvqPMLb3aqHIsSaQF4Lv1pPcpdkHc/edit

---

##  查看批改情况

### 方法一：即时查看学生作答

1. 打开编辑网址
2. 点击顶部 **「回复」** 标签
3. 查看所有学生的作答记录
4. 每道题的答案都会显示

### 方法二：统计分析报告

1. 点击顶部 **「分析」** 标签
2. 查看整体答对率
3. 查看每道题的正确率统计
4. 可导出Excel进行详细分析

### 方法三：设定自动评分（推荐）

1. 进入编辑界面
2. 点击顶部 **「设定」** → **「测验」**
3. 开启 **「将此表格设为测验」**
4. 在每道题下方点击 **「答案」**
5. 输入正确答案，系统会自动评分并显示给学生

---

## 📝 题目内容概览

### Section 1: 中文填充（15题）
- 来源: Chapter 7《要挑最大的》
- 词汇: 慕名、麦穗、不忿、宛如、踌躇等17个核心词
- 题型: 短答题（填空）

### Section 2: 中文语法（8题）
- 内容: 连接词、修辞手法
- 重点: 因为...所以、不仅...而且、明喻/比喻、拟人等

### Section 3: 英文语法（10题）
- Grammar 1: so 连接句（6题）
- Grammar 2: who/which 关系从句（4题）
- 来源: Unit 1 "A Helping Hand"

### Section 4: 常识生物分类（10题）
- 内容: 动物分类、植物分类
- 重点: 两栖类、爬行类、哺乳类、昆虫类、有花/无花植物

---

## 🔧 创建新表单的 Apps Script 代码

如需重新创建或修改表单，使用以下脚本：

```javascript
function createForm() {
  const form = FormApp.getActiveForm();
  
  // 清空现有题目
  const items = form.getItems();
  for (let i = items.length - 1; i >= 0; i--) {
    form.deleteItem(items[i]);
  }
  
  // Section 1: 中文填充（15题）
  form.insertItem(0, FormApp.newSectionHeader().setTitle('中文填充').build());
  const chineseVocab = [
    ['他________地来到这块麦田边，想拣到最大的一棵麦穗。', '慕名'],
    ['看到颗粒饱满的麦穗，有人想摘又________，总觉得后面还有更大的。', '不忿'],
    ['苏格拉底________地对学生说：「人生就是一次无法重复的选择。」', '语重心长'],
    ['阳光洒在麦田上，看起来________一片，非常美丽。', '金灿灿'],
    ['如果________了这个机会，以后可能就再也没有第二次了。', '错过'],
    ['经过反复思考，他才________明白到把握眼前最重要。', '恍然大悟'],
    ['这是我们________一次尝试的机会，一定要好好珍惜。', '唯一'],
    ['每棵麦穗都________的，看起来非常饱满。', '沉甸甸'],
    ['虽然前面还有更远的目标，但他知道这里就是旅程的________。', '尽头'],
    ['只要遵守学校的________，每个人都能安全通过走廊。', '规矩'],
    ['大家________地点头同意这个方案。', '不约而同'],
    ['这是一个难得的________，要把握时机。', '良机'],
    ['他犹豫不决地在两条路之间________。', '踌躇'],
    ['他最终决定________功名利禄，追求内心平静。', '舍弃'],
    ['漫长的人生路上，我们要学会坚持。', '漫长']
  ];
  
  for (const [q, a] of chineseVocab) {
    const item = form.addShortAnswerItem(q);
    item.setRequired(true);
    item.setDescription('答案：' + a);
  }
  
  // Section 2: 中文语法（8题）
  form.insertItem(form.getItems().length, FormApp.newSectionHeader().setTitle('中文语法').build());
  const chineseGrammar = [
    ['「他因为热爱阅读，所以每天都会去图书馆借书。」连接词是？', '因为...所以'],
    ['「她不仅会弹钢琴，而且还擅长画画。」连接词是？', '不仅...而且'],
    ['「即使下雨，我们也会按时到校上课。」连接词是？', '即使...也'],
    ['「她的笑容像阳光照进我的心里。」修辞手法？', '明喻/比喻'],
    ['「时间是流水，一去不再回。」修辞手法？', '暗喻/比喻'],
    ['「风儿轻轻地抚摸着我的脸颊。」修辞手法？', '拟人'],
    ['「他跑得像兔子一样快。」修辞手法？', '明喻/比喻'],
    ['「既...又...」是什么关系的连接词？', '并列']
  ];
  
  for (const [q, a] of chineseGrammar) {
    const item = form.addShortAnswerItem(q);
    item.setRequired(true);
    item.setDescription('答案：' + a);
  }
  
  // Section 3: 英文语法（10题）
  form.insertItem(form.getItems().length, FormApp.newSectionHeader().setTitle('英文语法').build());
  const englishGrammar = [
    ['I want to help the homeless. I prepare meals for them sometimes. (用 so 结合)', 'I want to help the homeless, so I prepare meals for them sometimes.'],
    ['She wants to raise money. She plans to go on a walkathon. (用 so 结合)', 'She wants to raise money, so she plans to go on a walkathon.'],
    ['He cares about the environment. He gives away old books to recycle. (用 so 结合)', 'He cares about the environment, so he gives away old books to recycle.'],
    ['The SPCA is an animal charity. It protects and saves animals. (用 which 结合)', 'The SPCA is an animal charity which protects and saves animals.'],
    ['Anna is a volunteer. She helps elderly people in need. (用 who 结合)', 'Anna is a volunteer who helps elderly people in need.'],
    ['The Doggy Inn is a special hotel. It lets guests take dogs for walks. (用 which 结合)', 'The Doggy Inn is a special hotel which lets guests take dogs for walks.'],
    ['Chris is a boy. He will sell flags for the blind next month. (用 who 结合)', 'Chris is a boy who will sell flags for the blind next month.'],
    ['The food charity provides meals. It serves people without homes. (用 which 结合)', 'The food charity provides meals which serves people without homes.'],
    ['We care about the elderly. We visit an elderly home every weekend. (用 so 结合)', 'We care about the elderly, so we visit an elderly home every weekend.'],
    ['Ben wants to help animals. He volunteers at the shelter. (用 so 结合)', 'Ben wants to help animals, so he volunteers at the shelter.']
  ];
  
  for (const [q, a] of englishGrammar) {
    const item = form.addShortAnswerItem(q);
    item.setRequired(true);
    item.setDescription('答案：' + a);
  }
  
  // Section 4: 常识生物分类（10题）
  form.insertItem(form.getItems().length, FormApp.newSectionHeader().setTitle('常识生物分类').build());
  const generalStudy = [
    ['蛙、蝾螈属于哪一类？', '两栖类'],
    ['蛇、海龟属于哪一类？', '爬行类'],
    ['蝙蝠、海豚属于哪一类？', '哺乳类'],
    ['蜜蜂属于哪一类（无脊椎动物）？', '昆虫类'],
    ['苔藓类和蕨类以什么繁殖？', '孢子'],
    ['有花植物与无花植物的主要分别是什么？', '有花植物会开花结果；无花植物永不开花'],
    ['凤凰木属于陆生还是水生植物？', '陆生植物'],
    ['睡莲属于陆生还是水生植物？', '水生植物'],
    ['鱼类用什么呼吸？', '鳃'],
    ['鸟类的身体特征是什么？', '全身长有羽毛']
  ];
  
  for (const [q, a] of generalStudy) {
    const item = form.addShortAnswerItem(q);
    item.setRequired(true);
    item.setDescription('答案：' + a);
  }
  
  FormApp.getUi().alert('✅ 表单已建立完成！共 ' + form.getItems().length + ' 题');
}
```

---

## 📱 使用建议

1. **手机/iPad 操作**: 直接点击作答网址即可开始练习
2. **分享给学生**: 复制作答网址发送给 Justan
3. **批改方式**: 
   - 简单练习: 直接在「回复」中查看
   - 正式测验: 开启「测验模式」自动评分
4. **复习错题**: 在「分析」中查看答错率高的题目

---

## 📁 相关文件位置

- 表单设置指南: `~/Desktop/openedujustan/google_form_guidance.md`
- CSV 模板: `~/Desktop/openedujustan/google_form_30min_training.csv`
- Apps Script 脚本: `~/Desktop/openedujustan/google_form_apps_script_fixed.js`
- HTML 互动游戏: `~/Desktop/openedujustan/General_Studies/bio_classification_game.html`
