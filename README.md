# 兆青MINI每日快报自动推送系统

## 项目简介

这是一个自动生成并推送每日快报的系统，包含天气、农历日期、限号和新闻等信息。

## 功能特点

- 自动获取天气信息（温度、风速、湿度、穿衣指数）
- 自动计算农历日期和节气
- 自动获取限号信息
- 自动获取国内外新闻（带链接）
- 自动推送到微信（通过Server酱）
- 定时执行（每天7:00、9:10、9:30）

## 部署到GitHub Actions

### 1. 创建GitHub仓库

1. 访问 https://github.com/
2. 创建新仓库，名称如：`zhaoqing-news`
3. 上传以下文件：
   - `generate_news.py`
   - `requirements.txt`
   - `.github/workflows/news.yml`

### 2. 配置Secrets

在仓库设置中添加以下Secrets：

- `SERVER_KEY`: Server酱的SendKey
- `NEWS_API_KEY`: 聚合数据的API密钥

### 3. 手动测试

在Actions页面手动触发workflow进行测试。

### 4. 自动运行

系统将在每天北京时间7:00、9:10、9:30自动运行。

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行脚本
python generate_news.py
```

## 配置说明

### Server酱配置

1. 访问 https://sct.ftqq.com/
2. 注册并获取SendKey
3. 关注Server酱公众号

### 聚合数据API配置

1. 访问 https://www.juhe.cn/
2. 注册并申请新闻API和天气API
3. 获取API密钥

## 注意事项

1. GitHub Actions使用UTC时间，北京时间需要减8小时
2. 免费额度足够日常使用
3. 建议将仓库设为Private保护API密钥

## 故障排查

如果推送失败：
1. 检查Actions日志
2. 确认Secrets配置正确
3. 验证API密钥是否有效
4. 检查脚本是否有语法错误

## 联系方式

兆青MINI工作室
专业MINI维修保养 • 升级 • 配件销售
