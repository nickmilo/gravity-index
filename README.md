# 🌟 Gravity Index for Obsidian

> Find your most important notes using the Integration at Scale methodology

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Obsidian Plugin](https://img.shields.io/badge/Obsidian-Compatible-7c3aed)](https://obsidian.md/)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-green)](https://claude.ai)

## 🚀 Quick Start (30 seconds)

### For Claude Code Users
1. Download `gravity_index.py` and place it in your Obsidian vault root
2. Open Claude Code in your vault directory
3. Ask Claude: *"Run the gravity index analysis and create the results note"*
4. Done! 🎉

### For Everyone Else
```bash
# In your Obsidian vault root
python3 gravity_index.py
```

## 🎯 What is the Gravity Index?

The Gravity Index identifies your most valuable notes using **Integration at Scale** methodology. Unlike simple link counting, it finds notes that:

- **Actively curate knowledge** (meaningful outgoing links)
- **Earn recognition** (reasonable incoming links)
- **Foster conversations** (bidirectional connections)
- **Maintain quality** (high efficiency ratios)

### Why It's Different

Traditional "most linked" analyses fail because they:
- ❌ Favor volume over value (1000 links to a daily note?)
- ❌ Ignore curation effort (outgoing links matter!)
- ❌ Miss conversational notes (bidirectional connections)
- ❌ Can't distinguish spam from substance

The Gravity Index solves this with:
- ✅ **Logarithmic scaling** - controls volume dominance
- ✅ **Sweet spot bonuses** - rewards meaningful scale (20-100 incoming)
- ✅ **Quality multipliers** - emphasizes efficiency over raw counts
- ✅ **Integration scoring** - values multi-dimensional strength

## 📊 Example Results

```markdown
1. **[[Habits Map]]** - Score: 388.7 (Scale+Curation+Conversation+Quality)
   - Raw: 56in, 34out, 24bi, 42.9%eff
   - Category: MOCs | Integration: 18.70
   - Components: Auth=101 | Cur=90 | Conv=72 | Qual=129 | Net=56 | Int=37

2. **[[Idea Emergence]]** - Score: 381.0 (Scale+Curation+Conversation+Quality)
   - Raw: 57in, 38out, 22bi, 38.6%eff
   - Category: MOCs | Integration: 17.96
   - Components: Auth=103 | Cur=93 | Conv=66 | Qual=116 | Net=62 | Int=36
```

## 🔧 How It Works

### Component Breakdown (100% total)
- **Authority (25%)**: log(incoming) × scale_bonus
- **Curation (20%)**: log(outgoing) × curation_bonus
- **Conversation (20%)**: bidirectional × conversation_bonus
- **Quality (15%)**: efficiency × quality_bonus
- **Network (10%)**: log(pagerank × 10000)
- **Integration (10%)**: √(bidirectional × outgoing × efficiency)

### Sweet Spot Bonuses
- **Scale Bonus (1.5x)**: 20-100 incoming links
- **Curation Bonus (1.3x)**: 15+ outgoing links
- **Conversation Bonus (1.2x)**: 10+ bidirectional links
- **Quality Bonus (2.0x)**: 25%+ efficiency ratio

## 📁 What You Get

After running the script:
- **`Gravity Index Results.md`** - Your top 50 notes analyzed
- Beautiful formatting with component breakdowns
- Category analysis and statistics
- Integration scores and efficiency ratings

## 🛠️ Requirements

- **Python 3.6+** (pre-installed on most systems)
- **Obsidian vault** with markdown files
- **[[Wiki links]]** format for connections
- No external dependencies! 🎉

## 💡 Use Cases

- **Find your best MOCs** - Maps of Content that truly integrate
- **Identify knowledge hubs** - Notes that connect diverse ideas
- **Audit your vault** - See what's actually valuable vs. just popular
- **Improve your notes** - Understand what makes notes valuable

## 🤝 Contributing

Found a bug? Have an idea? PRs welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📺 Video Tutorial

Watch the full explanation: [YouTube - "I Found My Most Important Notes with This One Script"](https://youtube.com/...)

## 🙏 Acknowledgments

- Inspired by the Obsidian community
- Integration at Scale methodology developed through analyzing 18,000+ notes
- Special thanks to Claude Code for seamless integration

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

*Made with ❤️ for the Obsidian community*