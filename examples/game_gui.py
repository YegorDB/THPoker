import tkinter

from thpoker.game import Player, Game


class GameGUI:
    collor_suit = {
        'c': '#A9D0F5',
        'd': '#F2F5A9',
        'h': '#F5A9A9',
        's': '#A9F5A9',
    }

    def __init__(self, chips=1000, blindes=[10, 20]):
        self._game = Game({"chips": chips, "blindes": blindes}, Player("Player"), Player("Computer"))
        self._reflections = {
            Game.ACTION_NEEDED: self.pre_action,
            Game.STAGE_NEEDED: self.pre_new_stage,
            Game.ROUND_NEEDED: self.pre_new_round,
            Game.THE_END: self.the_end,
        }
        self._new_parts = {
            Game.STAGE_NEEDED: self.new_stage,
            Game.ROUND_NEEDED: self.new_round,
        }
        self.get_window()
        self.new_round()
        self.window.mainloop()

    def get_window(self):
        self.window = tkinter.Tk()
        self.window.resizable(False, False)
        # background
        self.pict = tkinter.Canvas(self.window, width=500, height=400, bg='lightblue')
        self.pict.pack()
        for n in range(0, 500, 10):
            self.pict.create_line(n, 0, 500, 500-n, width=1, fill='blue')
            self.pict.create_line(0, n, 500-n, 500, width=1, fill='blue')
            self.pict.create_line(500-n, 0, 0, 500-n, width=1, fill='blue')
            self.pict.create_line(500, n, n, 500, width=1, fill='blue')
        # information
        self.pict.create_rectangle(15, 10, 385, 60, fill='#A9D0F5', outline='#A9D0F5')
        self.pict.create_rectangle(400, 135, 510, 265, fill='#A9D0F5', outline='#A9D0F5')
        for n in (0, 1):
            self.pict.create_rectangle(400, 80+n*195, 510, 125+n*195, fill='#A9D0F5', outline='#A9D0F5')
            self.pict.create_line(403, 185+n*30, 500, 185+n*30, width=1, fill='gray')
            self.pict.create_text(450, 100+n*195, text='Combination:', anchor='s')
            self.pict.create_text(425, 160+n*100, text='Chips:', anchor='s')
            self.pict.create_text(425, 180+n*60, text='Bet:', anchor='s')
        self.pict.create_text(425, 210, text='Bank:', anchor='s')       
        self.info = self.pict.create_text(200, 50, text='', anchor='s', font="Arial 24")
        self.opp_combo = self.pict.create_text(450, 120, text='', anchor='s')
        self.opp_chips = self.pict.create_text(475, 160, text='', anchor='s')
        self.opp_bet = self.pict.create_text(475, 180, text='', anchor='s')
        self.bank_vsl = self.pict.create_text(475, 210, text='', anchor='s')
        self.plr_bet = self.pict.create_text(475, 240, text='', anchor='s')
        self.plr_chips = self.pict.create_text(475, 260, text='', anchor='s')       
        self.plr_combo = self.pict.create_text(450, 315, text='', anchor='s')
        # table
        self.pict.create_rectangle(125, 90, 275, 310, fill='#B45F04', outline='#B45F04')
        self.pict.create_arc(165, 90, 385, 310, start=270, extent=180, fill='#B45F04', outline='#B45F04')
        self.pict.create_arc(15, 90, 235, 310, start=90, extent=180, fill='#B45F04', outline='#B45F04')
        self.pict.create_rectangle(125, 100, 275, 300, fill='darkgreen', outline='darkgreen')
        self.pict.create_arc(175, 100, 375, 300, start=270, extent=180, fill='darkgreen', outline='darkgreen')
        self.pict.create_arc(25, 100, 225, 300, start=90, extent=180, fill='darkgreen', outline='darkgreen')

    def print_info(self, players_data, state, bank, result):
        for player_data in players_data.values():
            if player_data["identifier"] == "Player":
                self.pict.itemconfig(self.plr_chips, text=str(player_data["chips"]))
                self.pict.itemconfig(self.plr_bet, text=str(player_data["stage_bets"]))
                if state == Game.SHOW_DOWN:
                    combo_name = str(player_data["combo"])
                    if len(result["winners"]) == 2:
                        result_name = "draw"
                    elif player_data["identifier"] in result["winners"]:
                        result_name = "win"
                    else:
                        result_name = "lose"
                    self.pict.itemconfig(self.info, text=result_name)
                else:
                    combo_name = ""
                self.pict.itemconfig(self.plr_combo, text=combo_name)
            else:
                self.pict.itemconfig(self.opp_chips, text=str(player_data["chips"]))
                self.pict.itemconfig(self.opp_bet, text=str(player_data["stage_bets"]))
                if state == Game.SHOW_DOWN:
                    self.draw_hand_cards(player_data, distr=False)
                    self.pict.itemconfig(self.opp_combo, text=str(player_data["combo"]))
                else:
                    self.pict.itemconfig(self.opp_combo, text='')
                    if player_data["last_action"]:
                        self.pict.itemconfig(self.info, text=f'Opponent has {player_data["last_action"].kind}') 
        self.pict.itemconfig(self.bank_vsl, text=str(bank))

    def draw_card(self, card, x, y, dx, tag):
        suit = self.collor_suit[card.suit.symbol]
        self.pict.create_rectangle(x+dx*60, y, x+40+dx*60, y+50, fill=suit, outline=suit, tag=tag)
        weight = card.weight.symbol
        self.pict.create_text(x+18+dx*60, y+52, text=weight, anchor='s', justify=tkinter.CENTER, font="Arial 30", tag=tag)
        self.pict.create_text(x+33+dx*60, y+18, text=card.suit.pretty_symbol, anchor='s', justify=tkinter.CENTER, font="Arial 16", tag=tag)

    def draw_tcard(self, table, stage_name):
        if stage_name == Game.Stage.FLOP:
            for n in range(3):
                self.draw_card(table[n], 60, 175, n, 'table')
        else:
            self.draw_card(table[-1], 60, 175, len(table)-1, 'table')

    def draw_hand_cards(self, player_data, distr=True):
        is_player = player_data["identifier"] == "Player"
        dy, tag = (130, 'phand') if is_player else (0, 'chand')
        if distr and not is_player:
            self.draw_hide_cards(dy, tag)
        else:
            for n in range(2):
                card = player_data["cards"][n]
                self.draw_card(card, 150, 110+dy, n, tag)

    def draw_hide_cards(self, dy, tag):
        for n in range(2):
            self.pict.create_rectangle(150+n*60, 110+dy, 190+n*60, 160+dy, fill='white', outline='white', tag=tag)
            self.pict.create_rectangle(152+n*60, 112+dy, 188+n*60, 158+dy, fill='#0489B1', outline='#0489B1', tag=tag)
            for i in range(0, 36, 6):
                self.pict.create_line(i+152+n*60, 112+dy, 188+n*60, 148-i+dy, width=1, fill='black', tag=tag)
                self.pict.create_line(152+n*60, i+122+dy, 188+n*60-i, 158+dy, width=1, fill='black', tag=tag)
                self.pict.create_line(2+i+152+n*60, 112+dy, 2+i+152+n*60, 158+dy, width=1, fill='black', tag=tag)
                self.pict.create_line(152+n*60, 117+dy, 188+n*60, 153+dy, width=1, fill='black', tag=tag)

    def refresh_table(self):
        self.pict.delete('chand')
        self.pict.delete('table')
        self.pict.delete('phand')

    def draw_fold(self):
        self.fold_but = tkinter.Button(
            self.window, height=3, width=10, bd=0,
            bg='#F5A9A9', activebackground='black', command=self.fold_react,
            text='fold', fg='black', activeforeground='white')
        self.fold_but.place(anchor='n', x=75, y=343)
        # def fold_collor1(event):
        #     self.fold_but['bg'] = '#FA5858'
        # self.fold_but.bind('<Enter>', fold_collor1)
        # def fold_collor2(event):
        #     self.fold_but['bg'] = '#F5A9A9'
        # self.fold_but.bind('<Leave>', fold_collor2)

    def fold_react(self):
        self.destroy_buttons()
        self.action(Player.Action.FOLD)

    def draw_callcheck(self, text, command):
        self.cll_chk_but = tkinter.Button(
            self.window, height=3, width=10, bd=0,
            bg='#A9F5A9', activebackground='black', command=command,
            text=text, fg='black', activeforeground='white')
        self.cll_chk_but.place(anchor='n', x=200, y=343)
        # def check_call_collor1(event):
        #     self.cll_chk_but['bg'] = '#58FA58'
        # self.cll_chk_but.bind('<Enter>', check_call_collor1)
        # def check_call_collor2(event):
        #     self.cll_chk_but['bg'] = '#A9F5A9'
        # self.cll_chk_but.bind('<Leave>', check_call_collor2)

    def check_react(self):
        self.destroy_buttons()
        self.action(Player.Action.CHECK)

    def call_react(self):
        self.destroy_buttons()
        self.action(Player.Action.CALL)

    def draw_raise(self, max_raise, dif):
        self.raise_but = tkinter.Button(
            self.window, height=3, width=10, bd=0,
            bg='#F2F5A9', activebackground='black', command=self.raise_react,
            text='raise', fg='black', activeforeground='white')
        self.raise_but.place(anchor='n', x=325, y=343)
        # def enter_rbut(event):
        #     self.raise_but['bg'] = '#F4FA58'
        # def leave_rbut(event):
        #     self.raise_but['bg'] = '#F2F5A9'
        # self.raise_but.bind('<Enter>', enter_rbut)
        # self.raise_but.bind('<Leave>', leave_rbut)
        self.raise_num = self.pict.create_rectangle(380, 343, 450, 394, fill='#F2F5A9', outline='#F2F5A9', tag='raise_num')
        self.pict.create_text(400, 358, text='max:', anchor='s', tag='raise_num')
        self.pict.create_text(430, 358, text=str(max_raise), anchor='s', tag='raise_num')
        self.pict.create_text(400, 394, text='min:', anchor='s', tag='raise_num')
        self.pict.create_text(430, 394, text=str(dif + 1), anchor='s', tag='raise_num')
        self.raise_ent = tkinter.Entry(self.window, width=5, bd=1)
        self.raise_ent.place(anchor='s', x=418, y=379)
        # def enter_rnum(event):
        #     self.pict.itemconfig(self.raise_num, fill='#F4FA58', outline='#F4FA58')
        # def leave_rnum(event):
        #     self.pict.itemconfig(self.raise_num, fill='#F2F5A9', outline='#F2F5A9')
        # self.pict.tag_bind('raise_num', '<Enter>', enter_rnum)
        # self.pict.tag_bind('raise_num', '<Leave>', leave_rnum)
        # self.raise_ent.bind('<Enter>', enter_rnum)
        # self.raise_ent.bind('<Leave>', leave_rnum)

    def raise_react(self):
        try:
            bet = int(self.raise_ent.get())
            self.destroy_buttons()
            self.action(Player.Action.RAISE, bet)
        except ValueError:
            self.pict.itemconfig(self.raise_num, fill='red', outline='red')
            self.window.focus()

    def draw_buttons(self, abilities=None, dif=None, point=None):
        if abilities:
            self.draw_fold()
            if abilities[Player.Action.CHECK]:
                self.draw_callcheck('check', self.check_react)
            else:
                self.draw_callcheck('call', self.call_react)
            if abilities[Player.Action.RAISE]:
                self.draw_raise(abilities[Player.Action.RAISE], dif)
        else:
            self.draw_callcheck('ok', self._new_parts[point])

    def destroy_buttons(self):
        try:
            self.cll_chk_but.destroy()
            self.fold_but.destroy()
            self.raise_but.destroy()
            self.raise_ent.destroy()
            self.pict.delete('raise_num')
        except AttributeError:
            pass
        self.pict.itemconfig(self.info, text='')

    def new_round(self):
        self.destroy_buttons()
        context = self._game.new_round()
        if context.success:
            self.refresh_table()
            self.new_stage()
        else:
            print("ERROR", context.description)

    def pre_new_round(self, context):
        if context.state == Game.ALL_IN:
            self.draw_distr_cards(context)
        self.print_info(context.players, context.state, context.bank, context.result)
        self.draw_buttons(point=context.point)
        # self.show_table()

    def new_stage(self):
        self.destroy_buttons()
        context = self._game.new_stage()
        self.reflect(context)

    def pre_new_stage(self, context):
        if context.state == Game.ALL_IN:
            self.draw_distr_cards(context)
        self.print_info(context.players, context.state, context.bank, context.result)
        self.draw_buttons(point=context.point)
        # self.show_table()

    def action(self, kind, bet=0):
        context = self._game.action(kind, bet)
        self.reflect(context)

    def draw_distr_cards(self, context):
        if context.stage_name == Game.Stage.PRE_FLOP:
            for player_data in context.players.values():
                self.draw_hand_cards(player_data)
        else:
            self.draw_tcard(context.table, context.stage_name)

    def pre_action(self, context):
        if context.players["current"]["identifier"] == "Player":
            if context.stage_depth in (0, 1):
                self.draw_distr_cards(context)
            self.print_info(context.players, context.state, context.bank, context.result)
            self.draw_buttons(context.players["current"]["abilities"], context.players["current"]["dif"])
            # self.show_table()
        else:
            kind, bet = self.computer_action(context)
            self.action(kind, bet)

    def computer_action(self, context):
        return Player.Action.FOLD, 0

    def reflect(self, context):
        if context.success:
            self._reflections[context.point](context)
        else:
            print("ERROR", context.description)

    def the_end(self, context):
        if context.state == Game.ALL_IN:
            self.draw_distr_cards(context)
        self.print_info(context.players, context.state, context.bank, context.result)
        # self.show_table()

#   def show_table(self):
#       def str_num(num):
#           result = str(num)
#           return ('_'*(4-len(result)) + result)

#       def str_card(cards):
#           result = ''
#           for card in cards:
#               result += card.weight.symbol + card.suit.symbol + ','
#           return (result[:-1])

#       title1 = '|plr|act|rais|bets|chps|hands|cmbo|'
#       for player in self.players:
#           inf = (player.action[:3] if player.action else '---',)
#           if player.action == 'raise':
#               inf += (str_num(player.lastbet),)
#           else:
#               inf += ('----',)
#           inf += (str_num(player.sbets), str_num(player.chips),)
#           if player.__class__.__name__ != 'Human' and not self.show_down:
#               inf += ('hide.',)
#           else:
#               inf += (str_card(player.hand.cards),)
#           inf += ('_'+player.combination.combo.combo+'_' if self.show_down else '----',)
#           if player.__class__.__name__ == 'Human':
#               you = '|you|' + '%s|'*6 % inf
#           else:
#               opp = '|opp|' + '%s|'*6 % inf
#       title2 = '|bank|_____table____|'
#       inf2 = '|'+str_num(self.players.bank())+'|'
#       if self.table.cards:
#           inf2 += str_card(self.table.cards)+'|'

#       print ('-'*35, title1, opp, you, '-'*35, title2, inf2, '-'*21+'\n', sep='\n')

if __name__ == "__main__":
    GameGUI()