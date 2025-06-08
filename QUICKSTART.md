# 🚀 Quick Start Guide

## For Claude Code Users (Recommended)

### 1. Download the Script
Download `gravity_index.py` from this repository

### 2. Place in Your Vault
Move the file to your Obsidian vault root directory (same level as your `.obsidian` folder)

### 3. Open Claude Code
Open Claude Code and navigate to your vault directory

### 4. Run the Analysis
Simply ask Claude:
> "Run the gravity index analysis and create the results note"

Claude will:
- Execute the script
- Show you progress
- Create a beautifully formatted results note
- Handle any errors gracefully

## For Terminal Users

### 1. Download and Place Script
Same as above - `gravity_index.py` goes in your vault root

### 2. Open Terminal
Navigate to your vault directory:
```bash
cd /path/to/your/obsidian/vault
```

### 3. Run the Script
```bash
python3 gravity_index.py
```

### 4. Check Your Results
Look for `Gravity Index Results.md` in your vault root

## What to Expect

The analysis will:
- Scan your entire vault (takes 5-30 seconds depending on size)
- Calculate Integration at Scale scores
- Generate a markdown report with your top 50 notes
- Show component breakdowns and statistics

## Example Output

```
🌟 Gravity Index Analyzer
==================================================
🔍 Scanning vault: /Users/you/ObsidianVault
📄 Found 5,234 markdown files
🔗 Found 8,421 unique note references
📊 Calculating Integration at Scale scores...
✅ Analysis complete!
📄 Results saved to: Gravity Index Results.md
🏆 Top note: Habits Map (Score: 388.7)
📊 Analyzed 3,256 notes with connections

🎯 Top 5 Notes:
  1. Habits Map: 388.7
  2. Idea Emergence: 381.0
  3. Knowledge MOC: 346.1
  4. Projects Hub: 317.8
  5. Daily Reviews: 304.7
```

## Troubleshooting

### "python3: command not found"
Try `python gravity_index.py` instead

### "No module named..." error
The script uses only Python standard library - no installation needed. Make sure you're using Python 3.6+

### No results or low scores
- Ensure your notes use `[[wiki links]]` format
- The script needs actual connections between notes to analyze
- Daily notes often score low (that's intentional!)

## Need Help?

- Check the main [README](README.md) for detailed methodology
- Watch the [YouTube tutorial](https://youtube.com/...)
- Open an issue on GitHub

Happy analyzing! 🎉