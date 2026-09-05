#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - AI Monopoly Game Engine
簡單版 Monopoly 遊戲引擎

功能：
1. 棋盤生成 (標準 40 格)
2. 玩家管理 (人類 + AI)
3. 擲骰子 + 移動
4. 基本交易系統
"""

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Property:
    """物業類"""
    name: str
    price: int
    rent: int
    owner: Optional[int] = None  # 玩家 ID
    level: int = 0  # 0=無, 1-3=屋, 4=酒店
    color_group: str = ""
    
    def get_rent(self):
        """計算租金"""
        base = self.rent
        if self.level == 1:
            return base * 2
        elif self.level == 2:
            return base * 4
        elif self.level == 3:
            return base * 7
        elif self.level == 4:
            return base * 10
        return base


@dataclass
class Player:
    """玩家類"""
    name: str
    player_id: int
    money: int = 1500
    position: int = 0
    properties: list = field(default_factory=list)
    in_jail: bool = False
    jail_turns: int = 0
    bankrupt: bool = False
    
    def can_afford(self, price: int) -> bool:
        return self.money >= price
    
    def pay(self, amount: int) -> bool:
        if self.can_afford(amount):
            self.money -= amount
            return True
        return False
    
    def receive(self, amount: int):
        self.money += amount
    
    def is_broke(self) -> bool:
        return self.money <= 0
    
    def total_assets(self) -> int:
        assets = self.money
        for prop in self.properties:
            assets += prop.price + (prop.level * prop.price // 2)
        return assets


class Board:
    """棋盤類"""
    
    def __init__(self):
        self.spaces: list[Property] = []
        self._create_board()
    
    def _create_board(self):
        """創建標準 40 格棋盤"""
        
        # GO 起點
        self.spaces.append(Property("GO", 0, 0))
        
        # 中低價物業 (藍色 -> 粉色)
        self.spaces.extend([
            Property("中環", 60, 10, color_group="blue"),
            Property("機會", 0, 0),
            Property("尖沙咀", 60, 10, color_group="blue"),
            Property("九龍城", 60, 10, color_group="blue"),
            Property("稅項", 0, 0),
            Property("旺角", 100, 15, color_group="light_blue"),
            Property("鐵路公司", 200, 25),
            Property("觀塘", 100, 15, color_group="light_blue"),
            Property("荃灣", 100, 15, color_group="light_blue"),
        ])
        
        # 監獄
        self.spaces.append(Property("監獄", 0, 0))
        
        # 中價物業 (綠色 -> 橙色)
        self.spaces.extend([
            Property("屯門", 140, 20, color_group="green"),
            Property("電力公司", 150, 30),
            Property("沙田", 140, 20, color_group="green"),
            Property("馬鞍山", 160, 25, color_group="green"),
            Property("命運", 0, 0),
            Property("紅磡", 180, 25, color_group="orange"),
            Property("港島線", 200, 30),
            Property("何文田", 180, 25, color_group="orange"),
            Property("油麻地", 180, 25, color_group="orange"),
        ])
        
        # 自由停車場
        self.spaces.append(Property("自由停車場", 0, 0))
        
        # 高價物業 (紅色 -> 深藍)
        self.spaces.extend([
            Property("銅鑼灣", 220, 35, color_group="red"),
            Property("機會", 0, 0),
            Property("灣仔", 220, 35, color_group="red"),
            Property("金鐘", 240, 40, color_group="red"),
            Property("稅項", 0, 0),
            Property("中環", 260, 50, color_group="yellow"),
            Property("鐵路公司", 200, 30),
            Property("上環", 260, 50, color_group="yellow"),
        ])
        
        # 監獄監房
        self.spaces.append(Property("入獄", 0, 0))
        
        # 最高價物業
        self.spaces.extend([
            Property("淺水灣", 300, 60, color_group="pink"),
            Property("命運", 0, 0),
            Property("南丫島", 300, 60, color_group="pink"),
            Property("迪士尼", 350, 70, color_group="dark_green"),
            Property("鐵路公司", 200, 30),
            Property("長洲", 320, 65, color_group="dark_green"),
            Property("機會", 0, 0),
            Property("太平山", 400, 100, color_group="dark_blue"),
        ])
        
        # 地皮王
        self.spaces.append(Property("地皮王", 0, 0))
    
    def get_space(self, index: int) -> Property:
        return self.spaces[index % len(self.spaces)]
    
    def print_board(self):
        """打印棋盤狀態"""
        print("\n" + "=" * 60)
        print("🎲 AI MONOPOLY - 棋盤狀態")
        print("=" * 60)
        for i, space in enumerate(self.spaces):
            if space.owner is not None:
                owner_str = f"[P{space.owner}]"
            else:
                owner_str = "   "
            print(f"{i:2d}. {owner_str} {space.name:15s} ${space.price}")
        print("=" * 60)


class Dice:
    """骰子类"""
    
    @staticmethod
    def roll():
        return random.randint(1, 6) + random.randint(1, 6)


class MonopolyGame:
    """主遊戲類"""
    
    def __init__(self, num_players: int = 4, test_mode: bool = False):
        self.board = Board()
        self.dice = Dice()
        self.players: list[Player] = []
        self.current_player: int = 0
        self.turn_count: int = 0
        self.game_over: bool = False
        self.test_mode = test_mode
        
        # 創建玩家
        names = ["你 (人類)", "AI 小聰", "AI 小明", "AI 小智"]
        for i in range(num_players):
            player = Player(
                name=names[i],
                player_id=i,
                money=1500
            )
            self.players.append(player)
    
    def get_current_player(self) -> Player:
        return self.players[self.current_player]
    
    def move_player(self, player: Player, steps: int):
        """移動玩家"""
        old_pos = player.position
        new_pos = (player.position + steps) % 40
        
        # 經過 GO 獲得報酬
        if new_pos < old_pos and new_pos != 0:
            player.receive(200)
            print(f"  🎉 經過 GO! +$200")
        
        player.position = new_pos
        
        # 處理落在特殊格子
        self.handle_landing(player)
    
    def handle_landing(self, player: Player):
        """處理落腳點"""
        space = self.board.get_space(player.position)
        
        print(f"\n  📍 {player.name} 落在 {space.name}")
        
        if space.name == "機會" or space.name == "命運":
            self.draw_card(player)
        elif space.name == "稅項":
            player.pay(100)
            print(f"  💸 繳稅 -$100")
        elif space.name == "入獄":
            player.in_jail = True
            player.jail_turns = 3
            print(f"  🔒 入獄！停留 3 回合")
        elif space.name == "監獄":
            print(f"  😌 只是訪問監獄")
        elif space.name == "自由停車場":
            player.receive(50)
            print(f"  🅿️ 停車費 +$50")
        elif space.name == "GO":
            player.receive(200)
            print(f"  🎉 到達 GO! +$200")
        elif space.name == "地皮王":
            print(f"  👑 地皮王！下一輪額外擲骰")
        elif space.owner is None:
            # 可以購買
            if player.can_afford(space.price):
                if self.test_mode:
                    # 測試模式自動購買
                    buy = True
                else:
                    buy = input(f"  是否購買 {space.name} ($ {space.price})? [y/n]: ")
                    buy = buy.lower() == 'y'
                if buy:
                    player.pay(space.price)
                    space.owner = player.player_id
                    player.properties.append(space)
                    print(f"  ✅ 購買成功!")
            else:
                print(f"  ❌ 資金不足，無法購買")
        elif space.owner != player.player_id:
            # 付租金
            rent = space.get_rent()
            owner = self.players[space.owner]
            if player.pay(rent):
                owner.receive(rent)
                print(f"  💰 支付租金 -$ {rent} 給 {owner.name}")
            else:
                print(f"  💔 破產了! {player.name} 被淘汰!")
                self.game_over = True
    
    def draw_card(self, player: Player):
        """抽卡"""
        cards = [
            ("前進 GO! +$200", lambda p: p.receive(200)),
            ("銀行錯誤退還 $50", lambda p: p.receive(50)),
            ("股票賺取 $100", lambda p: p.receive(100)),
            ("罰款 $75", lambda p: p.pay(75)),
            ("服務費用 $50", lambda p: p.pay(50)),
        ]
        card = random.choice(cards)
        card[1](player)
        print(f"  🃏 {card[0]}")
    
    def ai_decide_buy(self, player: Player, space: Property) -> bool:
        """AI 決定是否購買"""
        # 簡單 AI 策略
        if player.money > space.price * 2:
            return random.random() > 0.3  # 70% 機率購買
        elif player.money > space.price:
            return random.random() > 0.6  # 40% 機率購買
        return False
    
    def ai_turn(self, player: Player):
        """AI 回合 (增強版)"""
        print(f"\n{'='*55}")
        print(f"🤖 {player.name} | 💰${player.money} | 🏠{len(player.properties)}")
        print(f"{'='*55}")
        
        if player.in_jail:
            player.jail_turns -= 1
            if player.jail_turns <= 0:
                player.in_jail = False
                print(f"  🔓 出獄!")
            else:
                print(f"  🔒 仍在監獄 ({player.jail_turns} 回合)")
                self.next_player()
                return
        
        # 擲骰子
        rolls = self.dice.roll()
        print(f"  🎲 擲出 {rolls}")
        
        # 移動
        self.move_player(player, rolls)
        
        # 如果落在空地，AI 自動決定
        space = self.board.get_space(player.position)
        if space.owner is None and space.price > 0:
            if self.ai_decide_buy(player, space):
                if player.pay(space.price):
                    space.owner = player.player_id
                    player.properties.append(space)
                    print(f"  🤖 AI 購買 {space.name}!")
        
        self.next_player()
    
    def human_turn(self, player: Player):
        """人類回合"""
        print(f"\n{'='*50}")
        print(f"👤 {player.name} 嘅回合")
        print(f"💰 資金: ${player.money}")
        print(f"🏠 物業: {len(player.properties)} 個")
        print(f"{'='*50}")
        
        if player.in_jail:
            player.jail_turns -= 1
            if player.jail_turns <= 0:
                player.in_jail = False
                print(f"  🔓 出獄!")
            else:
                print(f"  🔒 仍在監獄 ({player.jail_turns} 回合)")
                self.next_player()
                return
        
        # 擲骰子
        if self.test_mode:
            rolls = self.dice.roll()
            print(f"  🎲 [測試模式] 你擲出 {rolls}")
        else:
            input("  🎲 按 Enter 擲骰子...")
            rolls = self.dice.roll()
            print(f"  🎲 你擲出 {rolls}")
        
        # 移動
        self.move_player(player, rolls)
        
        self.next_player()
    
    def next_player(self):
        """切換到下一個玩家"""
        self.current_player = (self.current_player + 1) % len(self.players)
        self.turn_count += 1
    
    def print_status(self):
        """打印所有玩家狀態"""
        print(f"\n📊 玩家狀態:")
        for player in self.players:
            status = f"  {player.name}: ${player.money}"
            if player.in_jail:
                status += " [🔒監獄]"
            print(status)
    
    def run_game(self, rounds: int = 30):
        """運行遊戲 (增強版)"""
        print("🎲 AI MONOPOLY v2.0")
        print(f"👥 玩家數量: {len(self.players)}")
        print(f"🎯 目標: 進行 {rounds} 回合\n")
        
        for round_num in range(rounds):
            print(f"\n{'#' * 60}")
            print(f"第 {round_num + 1} 回合")
            print(f"{'#' * 60}")
            
            for player in self.players:
                if self.game_over:
                    break
                
                if player.is_broke() or player.bankrupt:
                    print(f"  💔 {player.name} 破產淘汰!")
                    continue
                
                if player.player_id == 0 and not self.test_mode:
                    self.human_turn(player)
                else:
                    self.ai_turn(player)
            
            self.print_status()
        
        # 遊戲結束
        print(f"\n🏆 遊戲結束!")
        survivors = [p for p in self.players if not p.bankrupt]
        if survivors:
            winner = max(survivors, key=lambda p: p.total_assets())
            print(f"🎉 勝利者: {winner.name} (總資產: ${winner.total_assets()})")
        self.board.print_board()


if __name__ == "__main__":
    import sys
    test_mode = len(sys.argv) > 1 and sys.argv[1] == "--test"
    
    if test_mode:
        # 測試模式 (自動運行)
        game = MonopolyGame(num_players=4, test_mode=True)
        game.run_game(rounds=5)
    else:
        # 人類模式
        print("🎲 AI MONOPOLY")
        print("💡 提示: 使用 --test 參數自動測試")
