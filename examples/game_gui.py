# Copyright 2018 Yegor Bitensky

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import tkinter, random

from thpoker.game import Player, Game
from thpoker.core import Table, Hand, Combo


class ComputerAction:
    HANDS_RANGE = {
        'AA': 1.0,'KK': 0.995475113122172,'QQ': 0.9909502262443439,'JJ': 0.9864253393665159,'TT': 0.9819004524886877,'99': 0.9773755656108597,
        '88': 0.9728506787330317,'AKs': 0.9683257918552036,'AQs': 0.9653092006033183,'77': 0.9622926093514329,'AJs': 0.9577677224736049,
        'AKo': 0.9547511312217195,'ATs': 0.9457013574660633,'AQo': 0.942684766214178,'AJo': 0.9336349924585219,'KQs': 0.9245852187028658,
        '66': 0.9215686274509803,'A9s': 0.9170437405731523,'ATo': 0.9140271493212669,'KJs': 0.9049773755656109,'A8s': 0.9019607843137255,
        'KTs': 0.8989441930618401,'KQo': 0.8959276018099548,'A7s': 0.8868778280542986,'A9o': 0.8838612368024132,'KJo': 0.8748114630467572,
        '55': 0.8657616892911011,'QJs': 0.861236802413273,'K9s': 0.8582202111613876,'A6s': 0.8552036199095022,'A8o': 0.8521870286576169,
        'A5s': 0.8431372549019608,'KTo': 0.8401206636500754,'QTs': 0.8310708898944194,'A4s': 0.8280542986425339,'A7o': 0.8250377073906485,
        'K8s': 0.8159879336349924,'A3s': 0.8129713423831071,'QJo': 0.8099547511312217,'K9o': 0.8009049773755657,'A5o': 0.7918552036199095,
        'A6o': 0.7828054298642534,'Q9s': 0.7737556561085973,'K7s': 0.770739064856712,'JTs': 0.7677224736048266,'A2s': 0.7647058823529411,
        'QTo': 0.7616892911010558,'44': 0.7526395173453997,'A4o': 0.7481146304675717,'K6s': 0.7390648567119156,'Q8s': 0.7360482654600302,
        'K8o': 0.7330316742081447,'A3o': 0.7239819004524887,'K5s': 0.7149321266968326,'J9s': 0.7119155354449472,'Q9o': 0.7088989441930619,
        'JTo': 0.6998491704374057,'K7o': 0.6907993966817496,'K4s': 0.6817496229260935,'A2o': 0.6787330316742082,'Q7s': 0.669683257918552,
        'K6o': 0.6666666666666666,'K3s': 0.6576168929110106,'J8s': 0.6546003016591252,'T9s': 0.6515837104072398,'33': 0.6485671191553545,
        'Q6s': 0.6440422322775264,'Q8o': 0.6410256410256411,'K5o': 0.6319758672699849,'K2s': 0.6229260935143288,'J9o': 0.6199095022624435,
        'Q5s': 0.6108597285067874,'J7s': 0.6078431372549019,'K4o': 0.6048265460030166,'T8s': 0.5957767722473605,'Q7o': 0.5927601809954751,
        'Q4s': 0.583710407239819,'T9o': 0.5806938159879337,'J8o': 0.5716440422322775,'K3o': 0.5625942684766214,'Q6o': 0.5535444947209653,
        'Q3s': 0.5444947209653092,'98s': 0.5414781297134238,'J6s': 0.5384615384615384,'T7s': 0.5354449472096531,'K2o': 0.5324283559577677,
        '22': 0.5233785822021116,'Q5o': 0.5188536953242836,'Q2s': 0.5098039215686274,'J5s': 0.5067873303167421,'T8o': 0.5037707390648567,
        'J7o': 0.4947209653092006,'Q4o': 0.4856711915535445,'97s': 0.4766214177978884,'J4s': 0.473604826546003,'T6s': 0.47058823529411764,
        'Q3o': 0.4675716440422323,'J3s': 0.45852187028657615,'98o': 0.4555052790346908,'87s': 0.4464555052790347,'T7o': 0.4434389140271493,
        'J6o': 0.4343891402714932,'96s': 0.4253393665158371,'J2s': 0.42232277526395173,'Q2o': 0.4193061840120664,'T5s': 0.41025641025641024,
        'J5o': 0.4072398190045249,'T4s': 0.39819004524886875,'97o': 0.3951734539969834,'86s': 0.3861236802413273,'J4o': 0.38310708898944196,
        'T6o': 0.3740573152337858,'95s': 0.3650075414781297,'T3s': 0.36199095022624433,'76s': 0.358974358974359,'J3o': 0.3559577677224736,
        '87o': 0.3469079939668175,'T2s': 0.3378582202111614,'85s': 0.334841628959276,'96o': 0.33182503770739064,'J2o': 0.32277526395173456,
        'T5o': 0.3137254901960784,'94s': 0.3046757164404223,'75s': 0.30165912518853694,'T4o': 0.2986425339366516,'86o': 0.2895927601809955,
        '93s': 0.28054298642533937,'65s': 0.277526395173454,'84s': 0.27450980392156865,'95o': 0.27149321266968324,'T3o': 0.26244343891402716,
        '92s': 0.25339366515837103,'76o': 0.25037707390648567,'74s': 0.24132730015082957,'T2o': 0.2383107088989442,'54s': 0.22926093514328807,
        '64s': 0.22624434389140272,'85o': 0.22322775263951736,'83s': 0.21417797888386123,'94o': 0.21116138763197587,'75o': 0.20211161387631976,
        '82s': 0.19306184012066366,'73s': 0.19004524886877827,'93o': 0.1870286576168929,'65o': 0.1779788838612368,'53s': 0.1689291101055807,
        '63s': 0.16591251885369532,'84o': 0.16289592760180996,'92o': 0.15384615384615385,'43s': 0.14479638009049775,'74o': 0.14177978883861236,
        '72s': 0.13273001508295626,'54o': 0.1297134238310709,'64o': 0.12066365007541478,'52s': 0.11161387631975868,'62s': 0.1085972850678733,
        '83o': 0.10558069381598793,'82o': 0.09653092006033183,'42s': 0.08748114630467571,'73o': 0.08446455505279035,'53o': 0.07541478129713423,
        '63o': 0.06636500754147813,'32s': 0.05731523378582202,'43o': 0.05429864253393665,'72o': 0.04524886877828054,'52o': 0.03619909502262444,
        '62o': 0.027149321266968326,'42o': 0.01809954751131222,'32o': 0.00904977375565611,}

    def _get_bet(self, factor, context):
        bet = factor * (context.players[context.current_player]["dif"] or int(context.bank / 4))
        return \
            bet \
            if bet < context.players[context.current_player]["chips"] else \
            context.players[context.current_player]["chips"]

    def _get_percent(self, cof, bot, flat):
        if cof <= 1:
            return bot * cof
        elif cof <= 2:
            return bot + flat * 0.5 * (cof - 1)
        elif cof <= 3:
            return bot + flat * (0.25 + 0.5 * (cof - 2))
        elif cof <= 4:
            return bot + flat * (0.5 + 0.375 * (cof - 3))
        return 0.9

    def __call__(self, context):
        hand_range = self.HANDS_RANGE[context.players[context.current_player]["hand_type"]]
        cof = context.players[context.current_player]["dif"] / context.players[context.current_player]["round_bets"]
        top, bot, agr_bot, agr_mid = 0.9, 0.7, 0.6, 0.8
        flat = top - bot
        if context.stage_name is Game.Stage.PRE_FLOP:
            if cof:
                if hand_range > top:
                    return Player.Action.RAISE, self._get_bet(3, context)
                if hand_range >= self._get_percent(cof, bot, flat):
                    return (Player.Action.CALL,)
                return (Player.Action.FOLD,)
            else:
                if hand_range >= agr_bot:
                    factor = 3 if hand_range >= agr_mid else 2
                    return Player.Action.RAISE, self._get_bet(factor, context)
                else:
                    return (Player.Action.CHECK,)
        else:
            combo = Combo(
                table=Table(cards=context.table),
                hand=Hand(cards=context.players[context.current_player]["cards"]),
                nominal_check=True,
            )
            if cof:
                if combo.type > Combo.TWO_PAIRS and not combo.is_nominal:
                    return Player.Action.RAISE, self._get_bet(3, context)
                elif combo.type > Combo.HIGH_CARD and not combo.is_nominal or 0.5 * (hand_range + random.random()) >= cof:
                    return (Player.Action.CALL,)
                else:
                    return (Player.Action.FOLD,)
            else:
                if combo.type > Combo.HIGH_CARD and not combo.is_nominal:
                    return Player.Action.RAISE, self._get_bet(3, context)
                else:
                    return (Player.Action.CHECK,)


class ShellPrint:
    def _str_num(self, num):
        number = str(num)
        return f"{'_'*(4-len(number))}{number}"

    def _str_card(self, cards):
        return f"{str(cards)[1:-1].replace(' ', '')}"

    def _shell_show(self, context):
        for identifier, player_data in context.players.items():
            inf = (
                player_data["last_action"].kind[:3]
                if player_data["last_action"] else
                '---',
                self._str_num(player_data["last_action"].bet)
                if player_data["last_action"] is Player.Action.RAISE else
                '----',
                self._str_num(player_data["stage_bets"]),
                self._str_num(player_data["chips"]),
                self._str_card(player_data["cards"])
                if identifier is 'Player' or context.state in (Game.SHOW_DOWN, Game.ALL_IN, Game.THE_END) else
                '-----',
                f'-{player_data["combo"].short_name if context.state is Game.SHOW_DOWN else "--"}-',
            )
            if identifier is 'Player':
                player_info = f'|plr|{"|".join(inf)}'
            else:
                opponent_info = f'|opp|{"|".join(inf)}'
        common_info = f'|{self._str_num(context.bank)}|'
        if not context.stage_name is Game.Stage.PRE_FLOP:
            table = self._str_card(context.table)
            common_info += f'{table}{"-"*(14-len(table))}|'
        else:
            common_info += '--------------|'

        print(
            '-----------------------------------',
            '|idf|act|rais|bets|chps|hands|cmbo|',
            opponent_info,
            player_info,
            '-----------------------------------',
            '|bank|     table    |',
            common_info,
            '---------------------' + '\n',
            sep='\n',
        )


class DrawGameGUI:
    _collor_suit = {
        'c': '#A9D0F5',
        'd': '#F2F5A9',
        'h': '#F5A9A9',
        's': '#A9F5A9',
    }

    def _get_window(self):
        self._window = tkinter.Tk()
        self._window.resizable(False, False)
        # background
        self._pict = tkinter.Canvas(self._window, width=500, height=400, bg='lightblue')
        self._pict.pack()
        for n in range(0, 500, 10):
            self._pict.create_line(n, 0, 500, 500-n, width=1, fill='blue')
            self._pict.create_line(0, n, 500-n, 500, width=1, fill='blue')
            self._pict.create_line(500-n, 0, 0, 500-n, width=1, fill='blue')
            self._pict.create_line(500, n, n, 500, width=1, fill='blue')
        # information
        self._pict.create_rectangle(15, 10, 385, 60, fill='#A9D0F5', outline='#A9D0F5')
        self._pict.create_rectangle(400, 135, 510, 265, fill='#A9D0F5', outline='#A9D0F5')
        for n in (0, 1):
            self._pict.create_rectangle(40, 65+n*250, 360, 85+n*250, fill='#A9D0F5', outline='#A9D0F5')
            self._pict.create_line(403, 185+n*30, 500, 185+n*30, width=1, fill='gray')
            self._pict.create_text(55, 77+n*250, text='Combination:', anchor='w')
            self._pict.create_text(425, 160+n*100, text='Chips:', anchor='s')
            self._pict.create_text(425, 180+n*60, text='Bet:', anchor='s')
        self._pict.create_text(425, 210, text='Bank:', anchor='s')
        self._info = self._pict.create_text(200, 50, text='', anchor='s', font="Arial 24")
        self._opp_combo = self._pict.create_text(140, 77, text='', anchor='w')
        self._opp_chips = self._pict.create_text(475, 160, text='', anchor='s')
        self._opp_bet = self._pict.create_text(475, 180, text='', anchor='s')
        self._bank_vsl = self._pict.create_text(475, 210, text='', anchor='s')
        self._plr_bet = self._pict.create_text(475, 240, text='', anchor='s')
        self._plr_chips = self._pict.create_text(475, 260, text='', anchor='s')
        self._plr_combo = self._pict.create_text(140, 327, text='', anchor='w')
        # table
        self._pict.create_rectangle(125, 90, 275, 310, fill='#B45F04', outline='#B45F04')
        self._pict.create_arc(165, 90, 385, 310, start=270, extent=180, fill='#B45F04', outline='#B45F04')
        self._pict.create_arc(15, 90, 235, 310, start=90, extent=180, fill='#B45F04', outline='#B45F04')
        self._pict.create_rectangle(125, 100, 275, 300, fill='darkgreen', outline='darkgreen')
        self._pict.create_arc(175, 100, 375, 300, start=270, extent=180, fill='darkgreen', outline='darkgreen')
        self._pict.create_arc(25, 100, 225, 300, start=90, extent=180, fill='darkgreen', outline='darkgreen')

    def _print_info(self, players_data, state, bank, result):
        for identifier, player_data in players_data.items():
            if identifier is "Player":
                self._pict.itemconfig(self._plr_chips, text=str(player_data["chips"]))
                self._pict.itemconfig(self._plr_bet, text=str(player_data["stage_bets"]))
                if state in (Game.SHOW_DOWN, Game.THE_END):
                    if not result["loosers"]:
                        result_name = "draw"
                    elif identifier in result["winners"]:
                        result_name = "win"
                    else:
                        result_name = "lose"
                    self._pict.itemconfig(self._info, text=result_name)
                    self._pict.itemconfig(self._plr_combo, text=str(player_data["combo"]))
            else:
                self._pict.itemconfig(self._opp_chips, text=str(player_data["chips"]))
                self._pict.itemconfig(self._opp_bet, text=str(player_data["stage_bets"]))
                if state in (Game.SHOW_DOWN, Game.ALL_IN, Game.THE_END):
                    self._draw_hand_cards(identifier, player_data, distr=False)
                    if not state is Game.ALL_IN:
                        self._pict.itemconfig(self._opp_combo, text=str(player_data["combo"]))
                elif player_data["last_action"]:
                    self._pict.itemconfig(self._info, text=f'Opponent has {player_data["last_action"].kind}') 
        self._pict.itemconfig(self._bank_vsl, text=str(bank))

    def _draw_card(self, card, x, y, dx, tag):
        suit = self._collor_suit[card.suit.symbol]
        self._pict.create_rectangle(x+dx*60, y, x+40+dx*60, y+50, fill=suit, outline=suit, tag=tag)
        weight = card.weight.symbol
        self._pict.create_text(x+18+dx*60, y+52, text=weight, anchor='s', justify=tkinter.CENTER, font="Arial 30", tag=tag)
        self._pict.create_text(x+33+dx*60, y+18, text=card.suit.pretty_symbol, anchor='s', justify=tkinter.CENTER, font="Arial 16", tag=tag)

    def _draw_table_card(self, table, stage_name):
        if stage_name is Game.Stage.FLOP:
            for n in range(3):
                self._draw_card(table[n], 60, 175, n, 'table')
        else:
            self._draw_card(table[-1], 60, 175, len(table)-1, 'table')

    def _draw_hand_cards(self, identifier, player_data, distr=True):
        is_player = identifier is "Player"
        dy, tag = (130, 'phand') if is_player else (0, 'chand')
        if distr and not is_player:
            self._draw_hide_cards(dy, tag)
        else:
            for n in range(2):
                card = player_data["cards"][n]
                self._draw_card(card, 150, 110+dy, n, tag)

    def _draw_hide_cards(self, dy, tag):
        for n in range(2):
            self._pict.create_rectangle(150+n*60, 110+dy, 190+n*60, 160+dy, fill='white', outline='white', tag=tag)
            self._pict.create_rectangle(152+n*60, 112+dy, 188+n*60, 158+dy, fill='#0489B1', outline='#0489B1', tag=tag)
            for i in range(0, 36, 6):
                self._pict.create_line(i+152+n*60, 112+dy, 188+n*60, 148-i+dy, width=1, fill='black', tag=tag)
                self._pict.create_line(152+n*60, i+122+dy, 188+n*60-i, 158+dy, width=1, fill='black', tag=tag)
                self._pict.create_line(2+i+152+n*60, 112+dy, 2+i+152+n*60, 158+dy, width=1, fill='black', tag=tag)
                self._pict.create_line(152+n*60, 117+dy, 188+n*60, 153+dy, width=1, fill='black', tag=tag)

    def _refresh_table(self):
        self._pict.delete('chand')
        self._pict.delete('table')
        self._pict.delete('phand')
        self._pict.itemconfig(self._opp_combo, text='')
        self._pict.itemconfig(self._plr_combo, text='')

    def _draw_fold(self):
        self._fold_but = tkinter.Button(
            self._window, height=3, width=10, bd=0,
            bg='#F5A9A9', activebackground='black', command=self._fold_react,
            text='fold', fg='black', activeforeground='white')
        self._fold_but.place(anchor='n', x=75, y=343)
        self._fold_but.bind('<Enter>', self._change_fold_collor)
        self._fold_but.bind('<Leave>', self._change_fold_collor)
    
    def _change_fold_collor(self, event):
        self._fold_but['bg'] = '#FA5858' if event.type == '7' else '#F5A9A9'

    def _fold_react(self):
        self._destroy_buttons()
        self._action(Player.Action.FOLD)

    def _draw_callcheck(self, text, command):
        self._cll_chk_but = tkinter.Button(
            self._window, height=3, width=10, bd=0,
            bg='#A9F5A9', activebackground='black', command=command,
            text=text, fg='black', activeforeground='white')
        self._cll_chk_but.place(anchor='n', x=200, y=343)
        self._cll_chk_but.bind('<Enter>', self._change_call_check_collor)
        self._cll_chk_but.bind('<Leave>', self._change_call_check_collor)

    def _change_call_check_collor(self, event):
        self._cll_chk_but['bg'] = '#58FA58' if event.type == '7' else '#A9F5A9'

    def _check_react(self):
        self._destroy_buttons()
        self._action(Player.Action.CHECK)

    def _call_react(self):
        self._destroy_buttons()
        self._action(Player.Action.CALL)

    def _draw_raise(self):
        self._raise_but = tkinter.Button(
            self._window, height=3, width=10, bd=0,
            bg='#F2F5A9', activebackground='black', command=self._raise_react,
            text='raise', fg='black', activeforeground='white')
        self._raise_but.place(anchor='n', x=325, y=343)
        self.raise_num = self._pict.create_rectangle(380, 343, 450, 394, fill='#F2F5A9', outline='#F2F5A9', tag='raise_num')
        self._pict.create_text(400, 358, text='max:', anchor='s', tag='raise_num')
        self._pict.create_text(430, 358, text=str(self._current_max_raise), anchor='s', tag='raise_num')
        self._pict.create_text(400, 394, text='min:', anchor='s', tag='raise_num')
        self._pict.create_text(430, 394, text=str(self._current_min_raise), anchor='s', tag='raise_num')
        self._raise_ent = tkinter.Entry(self._window, width=5, bd=1)
        self._raise_ent.place(anchor='s', x=418, y=379)
        self._pict.tag_bind('raise_num', '<Enter>', self._change_raise_collor)
        self._pict.tag_bind('raise_num', '<Leave>', self._change_raise_collor)
        self._raise_ent.bind('<Enter>', self._change_raise_num_collor)
        self._raise_ent.bind('<Leave>', self._change_raise_num_collor)

    def _change_raise_collor(self, event):
        self._raise_but['bg'] = '#F4FA58' if event.type == '7' else '#F2F5A9'

    def _change_raise_num_collor(self, event):
        self._pict.itemconfig(
            self.raise_num,
            fill='#F4FA58' if event.type == '7' else '#F2F5A9',
            outline='#F4FA58' if event.type == '7' else '#F2F5A9')

    def _wrong_bet(self):
        self._pict.itemconfig(self.raise_num, fill='red', outline='red')
        self._window.focus()

    def _raise_react(self):
        try:
            bet = int(self._raise_ent.get())
            if bet > self._current_max_raise or bet < self._current_min_raise:
                self._wrong_bet()
            else:
                self._destroy_buttons()
                self._action(Player.Action.RAISE, bet)
        except ValueError:
            self._wrong_bet()

    def _draw_buttons(self, abilities=None, dif=None, point=None):
        if abilities:
            self._draw_fold()
            if abilities[Player.Action.CHECK]:
                self._draw_callcheck('check', self._check_react)
            else:
                self._draw_callcheck('call', self._call_react)
            if abilities[Player.Action.RAISE]:
                self._current_max_raise = abilities[Player.Action.RAISE]
                self._current_min_raise = dif + 1
                self._draw_raise()
        else:
            self._draw_callcheck('ok', self._new_parts[point])

    def _destroy_buttons(self):
        try:
            self._cll_chk_but.destroy()
            self._fold_but.destroy()
            self._raise_but.destroy()
            self._raise_ent.destroy()
            self._pict.delete('raise_num')
        except AttributeError:
            pass
        self._pict.itemconfig(self._info, text='')

    def _draw_distr_cards(self, context):
        if context.stage_name is Game.Stage.PRE_FLOP:
            for identifier, player_data in context.players.items():
                self._draw_hand_cards(identifier, player_data)
        else:
            self._draw_table_card(context.table, context.stage_name)


class GameGUI(DrawGameGUI, ShellPrint):
    def __init__(self, chips=1000, blindes=[10, 20]):
        self._game = Game({"chips": chips, "blindes": blindes}, Player("Player"), Player("Computer"))
        self._reflections = {
            Game.ACTION_NEEDED: self._pre_action,
            Game.STAGE_NEEDED: self._pre_new_stage,
            Game.ROUND_NEEDED: self._pre_new_round,
            Game.THE_END: self._the_end,
        }
        self._new_parts = {
            Game.STAGE_NEEDED: self._new_stage,
            Game.ROUND_NEEDED: self._new_round,
        }
        self._current_max_raise = chips
        self._current_min_raise = 0
        self._computer_action = ComputerAction()
        self._get_window()
        self._new_round()
        self._window.mainloop()

    def _pre_new_round(self, context):
        self._print_info(context.players, context.state, context.bank, context.result)
        self._draw_buttons(point=context.point)
        self._shell_show(context)

    def _new_round(self):
        if self._game.new_round().success:
            self._refresh_table()
            self._new_stage()
        else:
            print("ERROR", context.description)

    def _pre_new_stage(self, context):
        if context.state is Game.ALL_IN:
            self._draw_distr_cards(context)
        if context.state is Game.ALL_IN or context.current_player is "Computer":
            self._print_info(context.players, context.state, context.bank, context.result)
            self._draw_buttons(point=context.point)
            self._shell_show(context)
        else:
            self._new_stage()

    def _new_stage(self):
        self._destroy_buttons()
        context = self._game.new_stage()
        self._reflect(context)

    def _pre_action(self, context):
        self._shell_show(context)
        if context.current_player is "Player":
            if context.stage_depth == 0:
                self._draw_distr_cards(context)
            self._print_info(context.players, context.state, context.bank, context.result)
            self._draw_buttons(
                context.players[context.current_player]["abilities"],
                context.players[context.current_player]["dif"],
            )
        else:
            self._action(*self._computer_action(context))

    def _action(self, kind, bet=0):
        context = self._game.action(kind, bet)
        self._reflect(context)

    def _reflect(self, context):
        if context.success:
            self._reflections[context.point](context)
        else:
            print("ERROR", context.description)

    def _the_end(self, context):
        if context.state is Game.ALL_IN:
            self._draw_distr_cards(context)
        self._print_info(context.players, context.state, context.bank, context.result)
        self._shell_show(context)


if __name__ == "__main__":
    GameGUI()
