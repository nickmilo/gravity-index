#!/usr/bin/env python3
"""
Gravity Index Analyzer for Obsidian Vaults
Integration at Scale methodology - finds meaningful scale integrators

Usage: Place this script in your vault root and run:
python3 gravity_index.py

For Claude Code users: Just ask Claude to "Run the gravity index analysis"
"""

import os
import re
import math
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import json

class GravityIndexAnalyzer:
    def __init__(self, vault_path='.'):
        self.vault_path = Path(vault_path)
        self.notes = {}  # {note_name: file_path}
        self.links = defaultdict(set)  # {note: set of linked notes}
        self.backlinks = defaultdict(set)  # {note: set of notes linking to it}
        self.all_notes = set()
        
    def scan_vault(self):
        """Scan entire vault for notes and their links"""
        print(f"🔍 Scanning vault: {self.vault_path.absolute()}")
        
        # Skip common non-content folders
        skip_folders = {'.obsidian', '.git', 'node_modules', '__pycache__', '.DS_Store'}
        
        # Find all markdown files
        total_files = 0
        for md_file in self.vault_path.rglob('*.md'):
            # Skip if in excluded folder
            if any(skip_folder in md_file.parts for skip_folder in skip_folders):
                continue
                
            note_name = md_file.stem
            self.notes[note_name] = md_file
            self.all_notes.add(note_name)
            total_files += 1
            
        print(f"📄 Found {total_files} markdown files")
        
        # Extract links from all files
        for note_name, file_path in self.notes.items():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Find all [[wiki links]]
                wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
                
                for link in wiki_links:
                    # Handle aliases: [[note|alias]]
                    link_target = link.split('|')[0].strip()
                    
                    # Add to forward links
                    self.links[note_name].add(link_target)
                    
                    # Add to backlinks
                    self.backlinks[link_target].add(note_name)
                    
                    # Track all referenced notes
                    self.all_notes.add(link_target)
                    
            except Exception as e:
                print(f"⚠️  Error reading {file_path}: {e}")
                
        print(f"🔗 Found {len(self.all_notes)} unique note references")
        
    def calculate_pagerank(self, iterations=50, damping=0.85):
        """Calculate PageRank scores for all notes"""
        notes = list(self.all_notes)
        if not notes:
            return {}
            
        # Initialize PageRank values
        pagerank = {note: 1.0 / len(notes) for note in notes}
        
        # Iterate to convergence
        for _ in range(iterations):
            new_pagerank = {}
            
            for note in notes:
                # Base PageRank from damping
                new_pr = (1 - damping) / len(notes)
                
                # Add PageRank from linking notes
                for linking_note in self.backlinks.get(note, set()):
                    if linking_note in pagerank:
                        outgoing_count = len(self.links.get(linking_note, set()))
                        if outgoing_count > 0:
                            new_pr += damping * pagerank[linking_note] / outgoing_count
                
                new_pagerank[note] = new_pr
            
            pagerank = new_pagerank
            
        return pagerank
    
    def calculate_gravity_index(self):
        """Calculate Integration at Scale gravity scores"""
        print("📊 Calculating Integration at Scale scores...")
        
        gravity_scores = {}
        pagerank_scores = self.calculate_pagerank()
        
        # Collect all data for scaling
        all_data = []
        for note in self.all_notes:
            incoming = len(self.backlinks.get(note, set()))
            outgoing = len(self.links.get(note, set()))
            bidirectional = len(self.links.get(note, set()) & self.backlinks.get(note, set()))
            
            # Skip notes with no connections
            if incoming == 0 and outgoing == 0:
                continue
                
            # Apply logarithmic scaling to reduce volume dominance
            incoming_log = math.log(incoming + 1)
            outgoing_log = math.log(outgoing + 1)
            
            bidirectional_efficiency = bidirectional / max(incoming, 1) if incoming > 0 else 0
            
            # Sweet Spot Bonuses for meaningful scale integrators
            scale_bonus = 1.5 if 20 <= incoming <= 100 else 1.0
            curation_bonus = 1.3 if outgoing >= 15 else 1.0
            conversation_bonus = 1.2 if bidirectional >= 10 else 1.0
            quality_bonus = 2.0 if bidirectional_efficiency > 0.25 else 0.5
            
            # Integration index: multi-dimensional strength
            integration_index = math.sqrt(
                max(bidirectional, 1) * max(outgoing, 1) * max(bidirectional_efficiency, 0.01)
            )
            
            # PageRank with logarithmic scaling
            pagerank_log = math.log(pagerank_scores.get(note, 0) * 10000 + 1)
            
            # Determine category
            category = self._categorize_note(note)
            
            all_data.append({
                'note': note,
                'incoming': incoming,
                'outgoing': outgoing,
                'bidirectional': bidirectional,
                'incoming_log': incoming_log,
                'outgoing_log': outgoing_log,
                'bidirectional_efficiency': bidirectional_efficiency,
                'scale_bonus': scale_bonus,
                'curation_bonus': curation_bonus,
                'conversation_bonus': conversation_bonus,
                'quality_bonus': quality_bonus,
                'integration_index': integration_index,
                'pagerank_log': pagerank_log,
                'category': category,
                'exists': note in self.notes
            })
        
        if not all_data:
            print("❌ No notes with connections found!")
            return {}
            
        # Calculate 95th percentiles for normalization
        def get_95th_percentile(values):
            sorted_vals = sorted([v for v in values if v > 0])
            if not sorted_vals:
                return 1
            idx = int(0.95 * len(sorted_vals))
            return sorted_vals[min(idx, len(sorted_vals)-1)]
        
        p95_incoming_log = get_95th_percentile([d['incoming_log'] for d in all_data])
        p95_outgoing_log = get_95th_percentile([d['outgoing_log'] for d in all_data])
        p95_bidirectional = get_95th_percentile([d['bidirectional'] for d in all_data])
        p95_efficiency = get_95th_percentile([d['bidirectional_efficiency'] for d in all_data])
        p95_pagerank_log = get_95th_percentile([d['pagerank_log'] for d in all_data])
        p95_integration = get_95th_percentile([d['integration_index'] for d in all_data])
        
        # Calculate multipliers for target weights
        # Authority=25%, Curation=20%, Conversation=20%, Quality=15%, Network=10%, Integration=10%
        authority_multiplier = 25.0 / p95_incoming_log if p95_incoming_log > 0 else 0
        curation_multiplier = 20.0 / p95_outgoing_log if p95_outgoing_log > 0 else 0
        conversation_multiplier = 20.0 / p95_bidirectional if p95_bidirectional > 0 else 0
        quality_multiplier = 15.0 / p95_efficiency if p95_efficiency > 0 else 0
        network_multiplier = 10.0 / p95_pagerank_log if p95_pagerank_log > 0 else 0
        integration_multiplier = 10.0 / p95_integration if p95_integration > 0 else 0
        
        # Calculate final scores with bonuses
        for data in all_data:
            note = data['note']
            
            # Apply bonuses to base components
            authority_component = (data['incoming_log'] * data['scale_bonus']) * authority_multiplier
            curation_component = (data['outgoing_log'] * data['curation_bonus']) * curation_multiplier
            conversation_component = (data['bidirectional'] * data['conversation_bonus']) * conversation_multiplier
            quality_component = (data['bidirectional_efficiency'] * data['quality_bonus']) * quality_multiplier
            network_component = data['pagerank_log'] * network_multiplier
            integration_component = data['integration_index'] * integration_multiplier
            
            gravity = (authority_component + curation_component + conversation_component + 
                      quality_component + network_component + integration_component)
            
            gravity_scores[note] = {
                'total': gravity,
                'incoming': data['incoming'],
                'outgoing': data['outgoing'],
                'bidirectional': data['bidirectional'],
                'bidirectional_efficiency': data['bidirectional_efficiency'],
                'integration_index': data['integration_index'],
                'category': data['category'],
                'scale_bonus': data['scale_bonus'],
                'curation_bonus': data['curation_bonus'],
                'conversation_bonus': data['conversation_bonus'],
                'quality_bonus': data['quality_bonus'],
                'authority_component': authority_component,
                'curation_component': curation_component,
                'conversation_component': conversation_component,
                'quality_component': quality_component,
                'network_component': network_component,
                'integration_component': integration_component,
                'exists': data['exists']
            }
                
        return dict(sorted(gravity_scores.items(), key=lambda x: x[1]['total'], reverse=True))
    
    def _categorize_note(self, note):
        """Categorize notes based on name patterns"""
        if '⚗️' in note or 'LYT' in note:
            return 'LYT/Courses'
        elif 'MOC' in note:
            return 'MOCs'
        elif 'Map' in note:
            return 'Maps'
        elif 'Obsidian' in note:
            return 'Tools'
        elif any(word in note for word in ['Movie', 'Book', 'Series', 'Drama', 'Action', 'Comedy']):
            return 'Media'
        elif any(word in note for word in ['Workshop', 'Home', 'Pro', 'Hub']):
            return 'Workspaces'
        elif any(word in note for word in ['Project', 'Template', 'Record']):
            return 'Productivity'
        else:
            return 'Other'
    
    def _get_bonus_description(self, data):
        """Get a brief description highlighting strengths and potential gaps"""
        strengths = []
        gaps = []
        
        # Assess strengths
        if data['incoming'] >= 100:
            strengths.append("authoritative reference")
        elif data['incoming'] >= 50:
            strengths.append("widely referenced")
        elif data['incoming'] >= 20:
            strengths.append("solid authority")
            
        if data['outgoing'] >= 50:
            strengths.append("extensive curator")
        elif data['outgoing'] >= 25:
            strengths.append("active synthesizer")
        elif data['outgoing'] >= 15:
            strengths.append("knowledge weaver")
            
        if data['bidirectional'] >= 20:
            strengths.append("conversation hub")
        elif data['bidirectional'] >= 10:
            strengths.append("dialogue catalyst")
            
        if data['bidirectional_efficiency'] >= 0.4:
            strengths.append("selective depth")
        elif data['bidirectional_efficiency'] >= 0.25:
            strengths.append("quality focus")
            
        # Assess potential gaps
        if data['incoming'] < 10 and data['outgoing'] > 30:
            gaps.append("under-recognized")
        elif data['outgoing'] < 10 and data['incoming'] > 30:
            gaps.append("could link more")
        elif data['bidirectional'] < 5 and data['incoming'] > 20:
            gaps.append("one-way traffic")
            
        # Build description
        if strengths and gaps:
            return f"{', '.join(strengths[:2])}; {gaps[0]}"
        elif len(strengths) >= 2:
            return f"{strengths[0]} + {strengths[1]}"
        elif strengths:
            return strengths[0]
        elif data['integration_index'] > 10:
            return "balanced integrator"
        else:
            return "emerging connector"
    
    def generate_report(self, gravity_scores, top_n=50):
        """Generate formatted markdown report"""
        if not gravity_scores:
            return "# ❌ Gravity Index Results\n\nNo notes with connections found in this vault."
            
        report_lines = [
            f"# 🌟 Gravity Index Results",
            f"",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            f"",
            f"## Top {min(top_n, len(gravity_scores))} Notes by Gravity Index",
            f""
        ]
        
        # Add top notes
        for i, (note, data) in enumerate(list(gravity_scores.items())[:top_n]):
            description = self._get_bonus_description(data)
            report_lines.append(f"{i+1}. **[[{note}]]** - Score: {data['total']:.1f} - {description}")
        
        # Add summary statistics
        total_notes = len([n for n, d in gravity_scores.items() if d['exists']])
        avg_efficiency = sum(d['bidirectional_efficiency'] for d in gravity_scores.values()) / len(gravity_scores) * 100
        top_score = list(gravity_scores.values())[0]['total']
        
        # Category analysis
        categories = defaultdict(list)
        for note, data in list(gravity_scores.items())[:top_n]:
            categories[data['category']].append(data['total'])
        
        report_lines.extend([
            f"",
            f"---",
            f"",
            f"## Integration at Scale Methodology",
            f"",
            f"This analysis identifies **meaningful scale integrators** - notes that actively curate and engage at meaningful scale while maintaining conversational relationships.",
            f"",
            f"### Methodology Highlights",
            f"- **Logarithmic scaling** reduces pure volume dominance",
            f"- **Sweet spot bonuses** reward 20-100 incoming links (meaningful authority)",
            f"- **Quality multipliers** emphasize bidirectional efficiency over raw counts", 
            f"- **Integration index** rewards multi-dimensional strength",
            f"",
            f"### Component Weights",
            f"- **Authority (25%)**: log(incoming) × scale_bonus",
            f"- **Curation (20%)**: log(outgoing) × curation_bonus", 
            f"- **Conversation (20%)**: bidirectional × conversation_bonus",
            f"- **Quality (15%)**: efficiency × quality_bonus",
            f"- **Network (10%)**: log(pagerank × 10000)",
            f"- **Integration (10%)**: √(bidirectional × outgoing × efficiency)",
            f"",
            f"### Sweet Spot Bonuses",
            f"- **Scale Bonus (1.5x)**: 20-100 incoming links",
            f"- **Curation Bonus (1.3x)**: 15+ outgoing links", 
            f"- **Conversation Bonus (1.2x)**: 10+ bidirectional links",
            f"- **Quality Bonus (2.0x)**: 25%+ efficiency (bidirectional/incoming)",
            f"",
            f"---",
            f"",
            f"## Summary Statistics", 
            f"- **Total notes analyzed**: {len(gravity_scores):,}",
            f"- **Notes with files**: {total_notes:,}",
            f"- **Average efficiency**: {avg_efficiency:.1f}%",
            f"- **Top score**: {top_score:.1f}",
            f"",
            f"### Category Performance (Top {top_n})",
        ])
        
        for category, scores in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            avg_score = sum(scores) / len(scores)
            report_lines.append(f"- **{category}**: {len(scores)} notes (avg: {avg_score:.1f})")
        
        report_lines.extend([
            f"",
            f"---",
            f"",
            f"*Generated by Gravity Index Analyzer*",
            f"*Integration at Scale methodology identifies meaningful scale integrators*"
        ])
        
        return '\n'.join(report_lines)

def main():
    print("🌟 Gravity Index Analyzer")
    print("=" * 50)
    
    analyzer = GravityIndexAnalyzer()
    
    try:
        # Scan vault
        analyzer.scan_vault()
        
        if not analyzer.all_notes:
            print("❌ No markdown files found in vault!")
            return
        
        # Calculate gravity scores
        gravity_scores = analyzer.calculate_gravity_index()
        
        if not gravity_scores:
            print("❌ No notes with connections found!")
            return
        
        # Generate report
        report = analyzer.generate_report(gravity_scores)
        
        # Save report
        output_file = Path('Gravity Index Results.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Analysis complete!")
        print(f"📄 Results saved to: {output_file.absolute()}")
        print(f"🏆 Top note: {list(gravity_scores.keys())[0]} (Score: {list(gravity_scores.values())[0]['total']:.1f})")
        print(f"📊 Analyzed {len(gravity_scores)} notes with connections")
        
        # Show top 5
        print(f"\n🎯 Top 5 Notes:")
        for i, (note, data) in enumerate(list(gravity_scores.items())[:5]):
            print(f"  {i+1}. {note}: {data['total']:.1f}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()