import tkinter
from tkinter import DISABLED, StringVar, Canvas, NORMAL, BOTH, END
import requests
from letterFrequency import choose_letter
from high_scores import load_high_scores, write_data
from threading import Timer
from playsound import playsound

#Define Root window
master = tkinter.Tk()
master.resizable(0,0)
master.geometry('750x700')
master.title('Wordy-Purdy')

#Define colors and fonts
button_font=('Arial', 12)


#Define variables
grid = []
grid_size = 9
text = [[None]*grid_size for _ in range(grid_size)]
buttons = [[None]*grid_size for _ in range(grid_size)]
word_lst = []
buttons_pressed = []
scored_words_list = []
total_score = 0
begin = 0
high_score_list = load_high_scores()
start = 0
game_timer = 60

def one_second():
    global game_timer
    print("One second has passed")
    if game_timer > 0:
        game_timer -=1
        timer_display.config(text=game_timer)
        game_time()
    else:
        end_game_button.invoke()

def game_time():
    global t
    t = Timer(1 * 1, one_second)
    t.start()


def action(n, i):
    word_lst.append(text[n][i].get())
    print(text[n][i].get())
    buttons_pressed.append(buttons[n][i])
    buttons[n][i].config(state=DISABLED)
    ''.join(word_lst)
    current_word.config(text=word_lst)
    print(word_lst)
    # print(buttons_pressed)

def check_word():
    global word_lst

    print(word_lst)
    my_word = ''.join(word_lst)
    print(my_word.lower())

    word = my_word
    api_url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'.format(word=word)
    responce = requests.get(api_url)
    if responce.status_code == requests.codes.ok:
        print(responce.text)
        current_word.config(text='')
        playsound('correct-156911.mp3', block=False)
        word_lst.clear()
        buttons_pressed.clear()
        update_word_list(my_word)

    if '"title":"No Definitions Found"' in responce.text:
        print("Error:", responce.status_code, responce.text)
        playsound('negative-101682.mp3', block=False)
        current_word.config(text='')
        clear_word()


def clear_word():
    for button in range(len(buttons_pressed)):
        buttons_pressed[button].config(state=NORMAL)
    word_lst.clear()
    buttons_pressed.clear()

def update_word_list(word):
    scored_words = tkinter.Label(word_list_frame, text=word, pady=5, bg='#951e92', font=button_font, foreground='white')
    scored_words.pack()
    scored_words_list.append(scored_words)
    calculate_score(word)

def calculate_score(word):
    global total_score
    score = len(word)*2+len(word)
    total_score += score
    score_box.config(text=total_score)

def new_game():
    global game_timer
    global total_score
    global start
    game_timer = 60
    playsound('gotoast-102229.mp3', block=False)
    timer_display.config(text=game_timer)
    total_score = 0
    grid.clear()
    welcome_screen.grid_forget()
    new_game.config(state=DISABLED)
    end_game_button.config(state=NORMAL)
    score_box.config(text=total_score)
    # print(grid)
    # start = time.time()
    game_time()
    for i in range(len(scored_words_list)):
        scored_words_list[i].forget()
    generate_grid()

def generate_grid(destroy = 0):
    for n in range(0,grid_size):
        grid.append([])
        for i in range(0,grid_size):
            letter = choose_letter()
            text[n][i] = StringVar()
            text[n][i].set(letter)
            grid[n].append(Canvas(master, bg="#1E9522", height="56", width="56"))
            grid[n][i].propagate(False)
            grid[n][i].grid(row=n, column=i)
            buttons[n][i] = tkinter.Button(grid[n][i], textvariable = text[n][i], height=1, width=2, bg='#222', fg='white', state=NORMAL, command = lambda n=n, i=i : action(n, i))
            buttons[n][i].pack(pady=15)
            try:
                welcome_screen.grid_forget()
            except:
                welcome_screen.grid_forget()
            if destroy == 1:
                grid[n][i].grid_forget()
                buttons[n][i].grid_forget()
                scores_screen()

def end_game():
    global game_timer
    t.cancel()
    game_timer = 0
    timer_display.config(text=game_timer)
    name_for_high_score = check_high_score()
    generate_grid(1)
    grid.clear()
    new_game.config(state=NORMAL)
    end_game_button.config(state=DISABLED)

    if name_for_high_score != None:
        high_score_list[1].pop()
        high_score_list[1].insert(name_for_high_score, '')
        print(high_score_list[1])
        generate_grid(1)

        high_score_names[name_for_high_score].config(state=NORMAL)
        high_score_names[name_for_high_score].delete(0, END)
        high_score_names[name_for_high_score].insert(0, 'Enter your name')
        save_scores_button.config(state=NORMAL)


    # scores_screen()

def check_high_score():
    if total_score > min(high_score_list[0]):
        high_score_list[0].remove(min(high_score_list[0]))
        high_score_list[0].append(total_score)
        high_score_list[0].sort(reverse=True)
    # print(high_score_list[0], high_score_list[1])
        return high_score_list[0].index(total_score)
    return

def save_scores():
    save_scores_button.config(state=DISABLED)
    high_score_list[1].clear()
    count = 0
    for name in high_score_names:
        high_score_list[1].append(name.get())
        high_score_names[count].config(state=DISABLED)
        count+=1
    write_data(high_score_list[0], high_score_list[1])
    print(high_score_list[1])

#Show pre-game screen and high scores
def scores_screen(n=0):
    global welcome_screen
    global score1_entry, score2_entry, score3_entry, score4_entry, score5_entry
    global high_score_names
    global save_scores_button

    welcome_screen = tkinter.LabelFrame(master, width=526, height=525, bg='white')
    welcome_screen.grid(row=0, column=0)
    score_menu = tkinter.LabelFrame(welcome_screen, width=526, height=525, bg='#1E9522')
    score_menu.grid_propagate(False)
    score_menu.pack(padx=5, pady=5)

    rank_label = tkinter.Label(score_menu, text='Rank', bg='yellow', font=button_font)
    rank_label.grid(row=0, column=0, padx=(40,0), pady=(50,10))

    score_label = tkinter.Label(score_menu, text='score', bg='yellow', font=button_font)
    score_label.grid(row=0, column=0, padx=(180, 0), pady=(50,10))

    name_label = tkinter.Label(score_menu, text='Name', bg='yellow', font=button_font)
    name_label.grid(row=0, column=1, pady=(50,10), padx=70, sticky='w')

    high_score1_rank = tkinter.Label(score_menu, text='1.', bg='yellow', font=button_font)
    high_score1_score = tkinter.Label(score_menu, text=str(high_score_list[0][0]) , bg='yellow', font=button_font)
    high_score1_rank.grid(row=1, column=0, padx=(60,20), pady=(30,0))
    high_score1_score.grid(row=1, column=0,padx=(180,0),pady=(30,0))
    score1_entry = tkinter.Entry(score_menu, font=button_font, width=15)
    score1_entry.insert(0, high_score_list[1][0])
    score1_entry.config(state=DISABLED)
    score1_entry.grid(row=1, column=1, padx=50, pady=(30,0), sticky='W')

    high_score2_rank = tkinter.Label(score_menu, text='2.', bg='yellow', font=button_font)
    high_score2_score = tkinter.Label(score_menu, text=str(high_score_list[0][1]) , bg='yellow', font=button_font)
    high_score2_rank.grid(row=2, column=0, padx=(60,20), pady=(30,30))
    high_score2_score.grid(row=2, column=0,padx=(180,0),pady=(30,30))
    score2_entry = tkinter.Entry(score_menu, font=button_font, width=15)
    score2_entry.insert(0, high_score_list[1][1])
    score2_entry.config(state=DISABLED)
    score2_entry.grid(row=2, column=1, padx=50, pady=(30,30), sticky='W')

    high_score3_rank = tkinter.Label(score_menu, text='3.', bg='yellow', font=button_font)
    high_score3_score = tkinter.Label(score_menu, text=str(high_score_list[0][2]) , bg='yellow', font=button_font)
    high_score3_rank.grid(row=3, column=0, padx=(60,20), pady=(0,30))
    high_score3_score.grid(row=3, column=0,padx=(180,0),pady=(0,30))
    score3_entry = tkinter.Entry(score_menu, font=button_font, width=15)
    score3_entry.insert(0, high_score_list[1][2])
    score3_entry.config(state=DISABLED)
    score3_entry.grid(row=3, column=1, padx=50, pady=(0,30), sticky='W')

    high_score4_rank = tkinter.Label(score_menu, text='4.', bg='yellow', font=button_font)
    high_score4_score = tkinter.Label(score_menu, text=str(high_score_list[0][3]) , bg='yellow', font=button_font)
    high_score4_rank.grid(row=4, column=0, padx=(60,20), pady=(0,30))
    high_score4_score.grid(row=4, column=0,padx=(180,0),pady=(0,30))
    score4_entry = tkinter.Entry(score_menu, font=button_font, width=15)
    score4_entry.insert(0, high_score_list[1][3])
    score4_entry.config(state=DISABLED)
    score4_entry.grid(row=4, column=1, padx=50, pady=(0,30), sticky='W')

    high_score5_rank = tkinter.Label(score_menu, text='5.', bg='yellow', font=button_font)
    high_score5_score = tkinter.Label(score_menu, text=str(high_score_list[0][4]) , bg='yellow', font=button_font)
    high_score5_rank.grid(row=5, column=0, padx=(60,20), pady=(0,30))
    high_score5_score.grid(row=5, column=0,padx=(180,0),pady=(0,30))
    score5_entry = tkinter.Entry(score_menu, font=button_font, width=15)
    score5_entry.insert(0, high_score_list[1][4])
    score5_entry.config(state=DISABLED)
    score5_entry.grid(row=5, column=1, padx=50, pady=(0,30), sticky='W')

    save_scores_button = tkinter.Button(score_menu, text = "Save Scores", font=button_font, state=DISABLED, command=save_scores)
    save_scores_button.grid(row=6, column=0, padx = 200, pady=20, columnspan=2, ipadx=5, sticky='W')

    high_score_names = [score1_entry, score2_entry, score3_entry, score4_entry, score5_entry]
    #
    # if n == 1:
    #     # print(score1_entry.get())
    #     score1_entry.config(state=NORMAL)
    #     score1_entry.delete(0, END)
    #     score1_entry.insert(0, 'hi')


#Define layout grid and button variables
in_frame = tkinter.LabelFrame(master, padx=5, pady=10, bg='#951e91')
in_frame.grid(row=grid_size, column=0, columnspan=grid_size+1,  padx=5, pady=5, ipadx=20, sticky='WE')
# in_frame.grid_propagate(False)

word_list_frame = tkinter.LabelFrame(master, width=200, bg='#951e92')
word_list_frame.pack_propagate(False)
word_list_frame.grid(row=0, column=grid_size, padx=5, pady=(0,5), rowspan=grid_size+1, sticky="NS")
current_word = tkinter.Label(word_list_frame, text='Current Word', font=button_font , bg='#951e92', foreground='white', pady=20)
current_word.pack()

tkinter.Label(word_list_frame, text= "Entered Words", font=('button_font 16 underline') , bg='#951e92', foreground='white', pady=0).pack()

new_game = tkinter.Button(in_frame, text = "new game", font=button_font, command=new_game)
new_game.grid(row=0, column=0, padx=(80,10), pady=20)

end_game_button = tkinter.Button(in_frame, text = "end game", font=button_font, command=end_game)
end_game_button.grid(row=1, column=0, padx=(80,10), pady=10)

submit_button = tkinter.Button(in_frame, text='Submit word', font=button_font, command=check_word)
submit_button.grid(row=0, column=1, padx=10, pady=20)

clear_word_button = tkinter.Button(in_frame, text = "Clear word", font=button_font, command=clear_word)
clear_word_button.grid(row=0, column=2,  columnspan=2, padx=(10,0), pady=20, sticky='e')

score_text = tkinter.Label(in_frame, text= 'Score: ', font=button_font, foreground='white', bg='#951e92')
score_box = tkinter.Label(in_frame, text='0', font=button_font, foreground='white', bg='#951e92')
score_text.grid(row=1, column=1, columnspan=1, padx=35, sticky='w')
score_box.grid(row=1, column=1, columnspan=2, sticky='w', padx=85)

time_label = tkinter.Label(in_frame, text='Timer: ', font=button_font, foreground='white', bg='#951e92')
time_label.grid(row=1, column=2, columnspan=1, padx=15, sticky='ew')
timer_display = tkinter.Label(in_frame,text = game_timer, font=button_font, foreground='white', bg='#951e92')
timer_display.grid(row=1, column=2, columnspan=2, sticky='e')


scores_screen()
tkinter.mainloop()