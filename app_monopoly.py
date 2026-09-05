#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦀 Openhing - AI Monopoly Web App (Streamlit)
圖形界面版 Monopoly 遊戲

功能：
1. 擲骰子 + 移動
2. 購買物業
3. 收租
4. 建屋系統
5. AI 對手
"""

import streamlit as st
import random
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


# ==================== 數據模型 ====================

class PropertyType(Enum):
    PROPERTY = "property"
    RAILROAD = "railroad"
    UTILITY = "utility"
    TAX = "tax"
    CHANCE = "chance"
    COMMUNITY = "community"
    JAIL = "jail"
    FREE_PARKING = "free_parking"
    GO = "go"
    GO_TO_JAIL = "go_to_jail"


@dataclass
class Property:
    name: str
    price: int
    rent: int
    owner: Optional[int] = None
    level: int = 0
    color_group: str = ""
    property_type: PropertyType = PropertyType.PROPERTY
    
    def get_rent(self) -> int:
        if self.property_type == PropertyType.RAILROAD:
            count = sum(1 for p in game.board.spaces 
                      if p.property_type == PropertyType.RAILROAD and p.owner == self.owner)
            return 25 * (2 ** (count - 1))
        
        if self.property_type == PropertyType.UTILITY:
            return random.randint(1, 12) * 4
        
        base = self.rent
        multipliers = {0: 1, 1: 2, 2: 4, 3: 7, 4: 10}
        return base * multipliers.get(self.level, 1)
    
    def build_cost(self) -> int:
        if self.level < 4:
            return self.price // 2
        return 0


@dataclass
class Player:
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


# ==================== 棋盤 ====================

class Board:
    def __init__(self):
        self.spaces: list[Property] = []
        self._create_board()
    
    def _create_board(self):
        self.spaces.append(Property("GO", 0, 0, property_type=PropertyType.GO))
        self.spaces.extend([
            Property("中環", 60, 10, color_group="blue"),
            Property("機會", 0, 0, property_type=PropertyType.CHANCE),
            Property("尖沙咀", 60, 10, color_group="blue"),
            Property("九龍城", 60, 10, color_group="blue"),
            Property("利稅", 200, 0, property_type=PropertyType.TAX),
            Property("旺角", 100, 15, color_group="light_blue"),
            Property("港鐵公司", 200, 25, property_type=PropertyType.RAILROAD),
            Property("觀塘", 100, 15, color_group="light_blue"),
            Property("荃灣", 100, 15, color_group="light_blue"),
            Property("監獄", 0, 0, property_type=PropertyType.JAIL),
            Property("屯門", 140, 20, color_group="pink"),
            Property("電力公司", 150, 30, property_type=PropertyType.UTILITY),
            Property("沙田", 140, 20, color_group="pink"),
            Property("馬鞍山", 160, 25, color_group="pink"),
            Property("命運", 0, 0, property_type=PropertyType.COMMUNITY),
            Property("紅磡", 180, 25, color_group="orange"),
            Property("港島線", 200, 30, property_type=PropertyType.RAILROAD),
            Property("何文田", 180, 25, color_group="orange"),
            Property("油麻地", 180, 25, color_group="orange"),
            Property("自由停車場", 0, 0, property_type=PropertyType.FREE_PARKING),
            Property("銅鑼灣", 220, 35, color_group="red"),
            Property("機會", 0, 0, property_type=PropertyType.CHANCE),
            Property("灣仔", 220, 35, color_group="red"),
            Property("金鐘", 240, 40, color_group="red"),
            Property("遺產稅", 100, 0, property_type=PropertyType.TAX),
            Property("中環 CBD", 260, 50, color_group="yellow"),
            Property("東鐵線", 200, 30, property_type=PropertyType.RAILROAD),
            Property("上環", 260, 50, color_group="yellow"),
            Property("西營盤", 280, 55, color_group="yellow"),
            Property("入獄", 0, 0, property_type=PropertyType.GO_TO_JAIL),
            Property("淺水灣", 300, 60, color_group="green"),
            Property("命運", 0, 0, property_type=PropertyType.COMMUNITY),
            Property("南丫島", 300, 60, color_group="green"),
            Property("迪士尼樂園", 350, 70, color_group="green"),
            Property("機場快線", 200, 30, property_type=PropertyType.RAILROAD),
            Property("長洲", 320, 65, color_group="dark_green"),
            Property("機會", 0, 0, property_type=PropertyType.CHANCE),
            Property("太平山", 400, 100, color_group="dark_blue"),
            Property("地皮王", 0, 0, property_type=PropertyType.GO),
        ])
    
    def get_space(self, index: int) -> Property:
        return self.spaces[index % len(self.spaces)]


# ==================== 遊戲引擎 ====================

class Dice:
    @staticmethod
    def roll():
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return d1, d2, d1 + d2


class AIBrain:
    @staticmethod
    def should_buy(player: Player, property: Property) -> bool:
        ratio = player.money / property.price if property.price > 0 else 999
        if ratio < 1.5:
            return False
        elif ratio > 3:
            return random.random() > 0.2
        return random.random() > 0.5
    
    @staticmethod
    def should_build(player: Player, property: Property) -> bool:
        if property.level >= 4 or property.level == 0:
            return False
        cost = property.build_cost()
        if not player.can_afford(cost):
            return False
        same_color = [p for p in player.properties if p.color_group == property.color_group]
        if len(same_color) == len([p for p in game.board.spaces if p.color_group == property.color_group]):
            return True
        return random.random() > 0.6


class MonopolyGame:
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.players: list[Player] = []
        self.current_player: int = 0
        self.turn_count: int = 0
        self.game_over: bool = False
        self.go_collection = 0
        
        names = ["你 (人類)", "AI 巴菲特", "AI 索羅斯", "AI 達沃斯"]
        for i in range(4):
            player = Player(name=names[i], player_id=i)
            self.players.append(player)
    
    def move_player(self, player: Player, steps: int):
        old_pos = player.position
        new_pos = (player.position + steps) % 40
        
        if new_pos < old_pos and new_pos != 0:
            player.receive(200)
            st.success("🎉 經過 GO! +$200")
        
        player.position = new_pos
        self.handle_landing(player)
    
    def handle_landing(self, player: Player):
        space = self.board.get_space(player.position)
        st.info(f"📍 {player.name} → {space.name}")
        
        if space.property_type == PropertyType.CHANCE:
            self.draw_card(player, "機會")
        elif space.property_type == PropertyType.COMMUNITY:
            self.draw_card(player, "命運")
        elif space.property_type == PropertyType.TAX:
            fine = 100 if space.name == "利稅" else 200
            if player.pay(fine):
                self.go_collection += fine
                st.warning(f"💸 繳稅 -$ {fine}")
        elif space.property_type == PropertyType.GO_TO_JAIL:
            player.position = 10
            player.in_jail = True
            player.jail_turns = 3
            st.error("🔒 直接入獄!")
        elif space.property_type == PropertyType.FREE_PARKING:
            player.receive(self.go_collection)
            st.success(f"🅿️ 領取獎金 +$ {self.go_collection}")
            self.go_collection = 0
        elif space.property_type == PropertyType.GO:
            player.receive(200)
            st.success("🎉 到達 GO! +$200")
        elif space.owner is None and space.price > 0:
            self.try_purchase(player, space)
        elif space.owner is not None and space.owner != player.player_id:
            self.pay_rent(player, space)
    
    def try_purchase(self, player: Player, space: Property):
        if not player.can_afford(space.price):
            st.error(f"❌ 資金不足 (${space.price})")
            return
        
        # 使用 Streamlit 對話框
        confirm = st.confirm(f"是否購買 {space.name}? ($ {space.price})")
        
        if confirm:
            if player.pay(space.price):
                space.owner = player.player_id
                player.properties.append(space)
                st.success(f"✅ 購買成功!")
    
    def pay_rent(self, player: Player, space: Property):
        owner = self.players[space.owner]
        rent = space.get_rent()
        
        st.warning(f"💰 租金: $ {rent} ({owner.name})")
        
        if player.pay(rent):
            owner.receive(rent)
            st.success(f"✅ 支付成功")
        else:
            st.error(f"💔 破產了! {player.name} 被淘汰!")
            player.bankrupt = True
            self.game_over = True
    
    def draw_card(self, player: Player, card_type: str):
        cards = [
            ("前進 GO! +$200", lambda p: p.receive(200)),
            ("銀行退還 $50", lambda p: p.receive(50)),
            ("股票賺取 $100", lambda p: p.receive(100)),
            ("醫藥費 $50", lambda p: p.pay(50)),
            ("罰款 $75", lambda p: p.pay(75)),
            ("繼承遺產 $150", lambda p: p.receive(150)),
        ]
        card = random.choice(cards)
        card[1](player)
        st.info(f"🃏 [{card_type}] {card[0]}")
    
    def ai_turn(self, player: Player):
        with st.spinner(f"🤖 {player.name} 思考中..."):
            time.sleep(1)
            
        if player.in_jail:
            if random.random() > 0.5:
                player.in_jail = False
                st.info(f"🔓 {player.name} 成功出獄!")
            else:
                player.jail_turns -= 1
                st.info(f"🔒 {player.name} 仍在監獄 ({player.jail_turns} 回合)")
                self.next_player()
                return
        
        d1, d2, total = self.dice.roll()
        st.info(f"🎲 {player.name} 擲出 {d1}+{d2}={total}")
        
        self.move_player(player, total)
        
        # AI 嘗試建屋
        for prop in player.properties[:]:
            if AIBrain.should_build(player, prop):
                cost = prop.build_cost()
                if player.pay(cost):
                    prop.level += 1
                    st.info(f"🏗️ {prop.name} 建屋 (Lv.{prop.level})")
        
        self.next_player()
    
    def human_turn(self, player: Player):
        if player.in_jail:
            if st.checkbox(f"付費 $50 出獄?"):
                player.pay(50)
                player.in_jail = False
                st.success("🔓 出獄!")
            else:
                player.jail_turns -= 1
                st.info(f"🔒 服刑 ({player.jail_turns} 回合)")
                self.next_player()
                return
        
        if st.button("🎲 骰子"):
            d1, d2, total = self.dice.roll()
            st.info(f"🎲 你出 {d1}+{d2}={total}")
            self.move_player(player, total)
        
        self.next_player()
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % 4
        self.turn_count += 1
    
    def print_status(self):
        col1, col2, col3, col4 = st.columns(4)
        for i, player in enumerate(self.players):
            with col1 if i == 0 else (col2 if i == 1 else (col3 if i == 2 else col4)):
                status = f"{player.name}\n💰${player.money}\n🏠{len(player.properties)}個"
                if player.in_jail:
                    status += "\n🔒監獄"
                st.text(status)
    
    def run_game(self):
        st.title("🎲 AI MONOPOLY v2.0")
        
        current_player = self.players[self.current_player]
        
        if current_player.player_id == 0:
            self.human_turn(current_player)
        else:
            self.ai_turn(current_player)
        
        self.print_status()


# ==================== Streamlit App ====================

if __name__ == "__main__":
    game = MonopolyGame()
    game.run_game()
