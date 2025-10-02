#!/usr/bin/env python
"""
Quick fix for dataset feature names.
Changes "channel" to "channels" in video feature names.
"""

import json
import sys
from pathlib import Path

def fix_dataset_features(root_path: str):
    """Fix the feature names in info.json."""
    
    root = Path(root_path).expanduser()
    info_path = root / "meta" / "info.json"
    
    if not info_path.exists():
        print(f"✗ Error: {info_path} not found")
        return False
    
    # Backup original
    backup_path = info_path.with_suffix('.json.backup')
    
    # Read current info
    with open(info_path, 'r') as f:
        info = json.load(f)
    
    print("=" * 60)
    print("Fixing Dataset Features")
    print("=" * 60)
    print(f"Dataset: {root}")
    
    # Backup
    with open(backup_path, 'w') as f:
        json.dump(info, f, indent=4)
    print(f"✓ Backup created: {backup_path}")
    
    # Fix video feature names
    changes_made = False
    for feature_name, feature_def in info.get("features", {}).items():
        if feature_def.get("dtype") in ["video", "image"]:
            names = feature_def.get("names", [])
            
            # Handle dict format (old) - convert to list
            if isinstance(names, dict) and "axes" in names:
                old_names = names["axes"]
                print(f"✓ Converting {feature_name}: dict format -> list format")
                print(f"  Old: {names}")
                
                # Fix "channel" to "channels" and convert to list
                new_names = []
                for name in old_names:
                    if name == "channel":
                        new_names.append("channels")
                    else:
                        new_names.append(name)
                
                feature_def["names"] = new_names
                print(f"  New: {new_names}")
                changes_made = True
                
            # Handle list format (correct) - just fix channel->channels
            elif isinstance(names, list) and len(names) == 3:
                if names[2] == "channel":
                    print(f"✓ Fixing {feature_name}: {names} -> ", end="")
                    names[2] = "channels"
                    feature_def["names"] = names
                    print(names)
                    changes_made = True
                elif names[2] == "channels":
                    print(f"  {feature_name}: Already correct ({names})")
    
    if not changes_made:
        print("\n✓ No changes needed - all features already correct!")
        return True
    
    # Save fixed info
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=4)
    
    print("\n" + "=" * 60)
    print("✓ Dataset features fixed successfully!")
    print("=" * 60)
    print(f"Original backed up to: {backup_path}")
    print(f"Updated: {info_path}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_dataset_features.py <dataset_root>")
        print("Example: python fix_dataset_features.py ~/Robo_data/dobot_peg_lerobot")
        sys.exit(1)
    
    root_path = sys.argv[1]
    success = fix_dataset_features(root_path)
    
    if success:
        print("\nYou can now train with:")
        print("lerobot-train \\")
        print("  --dataset.repo_id=Josephzzz/dobot_peg_v3 \\")
        print(f"  --dataset.root={root_path} \\")
        print("  --dataset.video_backend=pyav \\")
        print("  --policy.type=act \\")
        print("  --output_dir=./ckpt/training \\")
        print("  --policy.device=cuda")
        sys.exit(0)
    else:
        sys.exit(1)

