from typing import Dict, Any, List, Tuple
from collections import Counter, defaultdict
from datetime import datetime
import re


def get_top_loyal_cards(player_data: Dict[str, Any], battle_log: List[Dict]) -> List[Dict[str, Any]]:
    """
    Get top 3 most used cards across all battles.
    """
    card_usage = Counter()
    
    # Count cards from battle log
    for battle in battle_log:
        # Check team deck (player's deck)
        team = battle.get('team', [])
        for player in team:
            cards = player.get('cards', [])
            for card in cards:
                card_name = card.get('name', '')
                if card_name:
                    card_usage[card_name] += 1
    
    # If no battle log data, use current deck from player data
    if not card_usage and 'currentDeck' in player_data:
        for card in player_data.get('currentDeck', []):
            card_name = card.get('name', '')
            if card_name:
                card_usage[card_name] = 1
    
    # Get top 3
    top_cards = card_usage.most_common(3)
    
    return [
        {"name": name, "count": count, "icon": f"https://cdn.clashroyale.com/cards/300/{name.lower().replace(' ', '')}.png"}
        for name, count in top_cards
    ]


def get_longest_win_streak(battle_log: List[Dict]) -> int:
    """
    Calculate longest win streak from battle log.
    """
    if not battle_log:
        return 0
    
    max_streak = 0
    current_streak = 0
    
    # Battle log is typically in reverse chronological order
    for battle in battle_log:
        team = battle.get('team', [])
        opponent = battle.get('opponent', [])
        
        # Determine if player won (team has more crowns or won)
        team_crowns = sum(p.get('crowns', 0) for p in team)
        opponent_crowns = sum(p.get('crowns', 0) for p in opponent)
        
        if team_crowns > opponent_crowns:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    return max_streak


def get_comeback_king_percentage(battle_log: List[Dict]) -> float:
    """
    Calculate percentage of wins where player was behind at some point.
    """
    if not battle_log:
        return 0.0
    
    comeback_wins = 0
    total_wins = 0
    
    for battle in battle_log:
        team = battle.get('team', [])
        opponent = battle.get('opponent', [])
        
        team_crowns = sum(p.get('crowns', 0) for p in team)
        opponent_crowns = sum(p.get('crowns', 0) for p in opponent)
        
        if team_crowns > opponent_crowns:
            total_wins += 1
            # Check if there was a comeback (simplified - if opponent had crowns first)
            # This is a simplified version - actual comeback detection would need more data
            if opponent_crowns > 0:
                comeback_wins += 1
    
    if total_wins == 0:
        return 0.0
    
    return round((comeback_wins / total_wins) * 100, 1)


def get_deck_archetype(player_data: Dict[str, Any], battle_log: List[Dict]) -> str:
    """
    Determine deck archetype based on cards and playstyle.
    """
    if not battle_log:
        # Use current deck if available
        if 'currentDeck' in player_data:
            cards = [c.get('name', '').lower() for c in player_data['currentDeck']]
        else:
            return "Unknown"
    else:
        # Get most common deck
        deck_counts = Counter()
        for battle in battle_log[:10]:  # Check last 10 battles
            team = battle.get('team', [])
            for player in team:
                cards = [c.get('name', '').lower() for c in player.get('cards', [])]
                if cards:
                    deck_counts[tuple(sorted(cards))] += 1
        
        if not deck_counts:
            return "Unknown"
        
        most_common_deck = deck_counts.most_common(1)[0][0]
        cards = list(most_common_deck)
    
    # Simple archetype detection based on card names
    card_names_str = ' '.join(cards)
    
    # Check for cycle cards
    cycle_cards = ['skeleton', 'goblin', 'ice spirit', 'fire spirit', 'bats']
    if any(card in card_names_str for card in cycle_cards):
        cycle_count = sum(1 for card in cycle_cards if any(card in c for c in cards))
        if cycle_count >= 3:
            return "Cycle"
    
    # Check for beatdown
    beatdown_cards = ['golem', 'giant', 'pekka', 'lava hound', 'royal giant']
    if any(card in card_names_str for card in beatdown_cards):
        return "Beatdown"
    
    # Check for control
    control_cards = ['x-bow', 'mortar', 'tesla', 'inferno']
    if any(card in card_names_str for card in control_cards):
        return "Control"
    
    # Check for bridge spam
    spam_cards = ['bandit', 'royal ghost', 'dark prince', 'battle ram']
    if any(card in card_names_str for card in spam_cards):
        return "Bridge Spam"
    
    return "Balanced"


def get_rare_gem(battle_log: List[Dict]) -> Dict[str, Any]:
    """
    Find a rarely used card that has high win rate when used.
    """
    if not battle_log:
        return {"name": "N/A", "win_rate": 0, "usage": 0}
    
    card_stats = defaultdict(lambda: {"wins": 0, "uses": 0})
    
    for battle in battle_log:
        team = battle.get('team', [])
        opponent = battle.get('opponent', [])
        
        team_crowns = sum(p.get('crowns', 0) for p in team)
        opponent_crowns = sum(p.get('crowns', 0) for p in opponent)
        won = team_crowns > opponent_crowns
        
        for player in team:
            cards = player.get('cards', [])
            for card in cards:
                card_name = card.get('name', '')
                if card_name:
                    card_stats[card_name]["uses"] += 1
                    if won:
                        card_stats[card_name]["wins"] += 1
    
    # Find card with low usage but high win rate
    rare_gem = None
    best_score = 0
    
    for card_name, stats in card_stats.items():
        if stats["uses"] >= 2:  # At least used twice
            win_rate = (stats["wins"] / stats["uses"]) * 100 if stats["uses"] > 0 else 0
            # Score based on win rate and inverse of usage
            score = win_rate / max(stats["uses"], 1)
            if score > best_score and stats["uses"] <= 5:  # Rarely used
                best_score = score
                rare_gem = {
                    "name": card_name,
                    "win_rate": round(win_rate, 1),
                    "usage": stats["uses"]
                }
    
    return rare_gem or {"name": "N/A", "win_rate": 0, "usage": 0}


def get_nemesis(battle_log: List[Dict]) -> Dict[str, Any]:
    """
    Find opponent that player faces most often and track wins/losses.
    """
    if not battle_log:
        return {"name": "N/A", "tag": "N/A", "wins": 0, "losses": 0, "total": 0}
    
    opponent_stats = defaultdict(lambda: {"name": "", "tag": "", "wins": 0, "losses": 0, "total": 0})
    
    for battle in battle_log:
        team = battle.get('team', [])
        opponent = battle.get('opponent', [])
        
        team_crowns = sum(p.get('crowns', 0) for p in team)
        opponent_crowns = sum(p.get('crowns', 0) for p in opponent)
        
        for opp in opponent:
            opp_name = opp.get('name', 'Unknown')
            opp_tag = opp.get('tag', '')
            if opp_tag:
                opponent_stats[opp_tag]["name"] = opp_name
                opponent_stats[opp_tag]["tag"] = opp_tag
                opponent_stats[opp_tag]["total"] += 1
                
                if team_crowns > opponent_crowns:  # Player won
                    opponent_stats[opp_tag]["wins"] += 1
                elif opponent_crowns > team_crowns:  # Player lost
                    opponent_stats[opp_tag]["losses"] += 1
    
    if not opponent_stats:
        return {"name": "N/A", "tag": "N/A", "wins": 0, "losses": 0, "total": 0}
    
    # Get opponent with most total battles (most frequent opponent)
    nemesis = max(opponent_stats.items(), key=lambda x: x[1]["total"])
    return nemesis[1]


def get_peak_performance_hours(battle_log: List[Dict]) -> Dict[str, Any]:
    """
    Determine peak performance hours based on win rate by hour.
    """
    if not battle_log:
        return {"hour": "N/A", "win_rate": 0}
    
    hour_stats = defaultdict(lambda: {"wins": 0, "total": 0})
    
    for battle in battle_log:
        battle_time = battle.get('battleTime', '')
        if battle_time:
            try:
                # Parse ISO format timestamp (format: 20240101T120000.000Z)
                # Remove milliseconds and Z, then parse
                clean_time = re.sub(r'\.\d+', '', battle_time.replace('Z', ''))
                dt = datetime.strptime(clean_time, '%Y%m%dT%H%M%S')
                hour = dt.hour
                
                team = battle.get('team', [])
                opponent = battle.get('opponent', [])
                team_crowns = sum(p.get('crowns', 0) for p in team)
                opponent_crowns = sum(p.get('crowns', 0) for p in opponent)
                
                hour_stats[hour]["total"] += 1
                if team_crowns > opponent_crowns:
                    hour_stats[hour]["wins"] += 1
            except:
                continue
    
    if not hour_stats:
        return {"hour": "N/A", "win_rate": 0}
    
    # Find hour with best win rate (minimum 3 battles)
    best_hour = None
    best_win_rate = 0
    
    for hour, stats in hour_stats.items():
        if stats["total"] >= 3:
            win_rate = (stats["wins"] / stats["total"]) * 100
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_hour = hour
    
    if best_hour is None:
        return {"hour": "N/A", "win_rate": 0}
    
    # Format hour
    hour_str = f"{best_hour}:00"
    if best_hour < 12:
        hour_str += " AM"
    else:
        hour_str = f"{best_hour - 12 if best_hour > 12 else best_hour}:00 PM"
    
    return {"hour": hour_str, "win_rate": round(best_win_rate, 1)}


def get_trophy_roller_coaster(player_data: Dict[str, Any], battle_log: List[Dict]) -> Dict[str, Any]:
    """
    Calculate trophy history and biggest swings.
    """
    current_trophies = player_data.get('trophies', 0)
    best_trophies = player_data.get('bestTrophies', current_trophies)
    
    # Calculate trophy changes from battle log
    trophy_changes = []
    if battle_log:
        for battle in battle_log[:25]:  # Last 25 battles
            team = battle.get('team', [])
            opponent = battle.get('opponent', [])
            team_crowns = sum(p.get('crowns', 0) for p in team)
            opponent_crowns = sum(p.get('crowns', 0) for p in opponent)
            
            # Estimate trophy change (simplified)
            if team_crowns > opponent_crowns:
                trophy_changes.append(30)  # Win
            else:
                trophy_changes.append(-30)  # Loss
    
    biggest_gain = max(trophy_changes) if trophy_changes else 0
    biggest_loss = min(trophy_changes) if trophy_changes else 0
    total_swing = abs(biggest_gain) + abs(biggest_loss) if trophy_changes else 0
    
    return {
        "current": current_trophies,
        "best": best_trophies,
        "biggest_gain": biggest_gain,
        "biggest_loss": biggest_loss,
        "total_swing": total_swing,
        "recent_changes": trophy_changes[-10:] if trophy_changes else []
    }


def analyze_player(player_data: Dict[str, Any], battle_log: List[Dict]) -> Dict[str, Any]:
    """
    Generate all insights for a player.
    """
    nemesis_data = get_nemesis(battle_log)
    
    # Determine nemesis relationship message
    nemesis_message = ""
    if nemesis_data["name"] != "N/A" and nemesis_data["total"] > 0:
        if nemesis_data["wins"] > nemesis_data["losses"]:
            nemesis_message = f"{nemesis_data['name']} is your bitch"
        elif nemesis_data["losses"] > nemesis_data["wins"]:
            nemesis_message = f"You are {nemesis_data['name']}'s bitch"
        else:
            nemesis_message = f"Evenly matched with {nemesis_data['name']}"
    
    return {
        "top_loyal_cards": get_top_loyal_cards(player_data, battle_log),
        "longest_win_streak": get_longest_win_streak(battle_log),
        "comeback_king_percentage": get_comeback_king_percentage(battle_log),
        "deck_archetype": get_deck_archetype(player_data, battle_log),
        "rare_gem": get_rare_gem(battle_log),
        "nemesis": {**nemesis_data, "message": nemesis_message},
        "peak_performance_hours": get_peak_performance_hours(battle_log),
        "trophy_roller_coaster": get_trophy_roller_coaster(player_data, battle_log),
        "player_name": player_data.get('name', 'Unknown'),
        "player_tag": player_data.get('tag', ''),
    }

