print("Status: Initializing...")
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

import io
import re
import math
import string
from collections import Counter
from nltk.util import ngrams
from nltk.tokenize import regexp_tokenize

class SpellcheckerGUI(tk.Tk):
	
	def __init__(self):
		"""
		Initializing the GUI components and reading in,
		(cleaning?), and creation of unigrams and dictionary.
		"""
		super(SpellcheckerGUI, self).__init__()
		self.title("Spellchecking GUI")
		self.minsize(800, 600)
		
		# reading in the corpus and dictionary
		with io.open("clean_economics.txt", "r", encoding = "utf-16") as f:
			self.corpus = f.read()
		with io.open("dictionary.txt", "r", encoding = "utf-16") as f:
			dict_text = f.read()
		
		# create unigram model
		self.unigrams = self.corpus.split(' ')
		N_u = len(self.unigrams)
		self.counts_u = dict(Counter(self.unigrams))
	
		model_u = {}
		for (key,value) in zip(self.counts_u.keys(), self.counts_u.values()):
			model_u[key] = value/N_u
		self.model_u = model_u

		# create dictionary list 
		self.dictionary = sorted(set(dict_text.split('\n')))
		self.non_words = [] #empty list of non-words

		# create left bigrams (the usual bigram), right bigrams and trigrams
		self.bigramsl = list(ngrams(self.unigrams, 2))
		self.bigramsr = [(w1,w2) for (w1,w2) in zip(self.unigrams[1:],
													self.unigrams[:-1])]
		self.counts_bl = dict(Counter(self.bigramsl))
		self.counts_br = dict(Counter(self.bigramsr))
		N_b = len(self.bigramsl)

		self.trigrams = list(ngrams(self.unigrams, 3))
		self.counts_t = dict(Counter(self.trigrams))

		self.create_layout()
		print("\nStatus: Ready\n")

		
	def create_layout(self):
		"""
		This is where the layout of the GUI is created.
		"""
		
		# what to add in menu bar?
		menu = tk.Menu()
		self.config(menu=menu)
		#menu.add_cascade(label="Menu",menu=subMenu)

		# Spread out the canvas and the frame
		HEIGHT=800
		WIDTH=900
		canvas = tk.Canvas(height=HEIGHT,width=WIDTH)
		canvas.pack()
		self.frame = tk.Frame(bg='#AFAFAF', bd=1) # this is the gray frame
		self.frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor='n')
		

		# Provide instructions to the user
		mylabel1 = tk.Label(self.frame,text= "Please enter words here...", bg='#AFAFAF',
							fg="black",font="none 10 normal")
		mylabel1.place(relx=0.1, rely=0.05)
		
		# This is the big text box where user puts in their input
		self.txt1 = scrolledtext.ScrolledText(self.frame,bg="white", width=50,font="Arial 10")
		self.txt1.focus()
		self.txt1.pack(expand=True, fill='both')
		self.txt1.place(relx=0.1, rely= 0.1, relwidth=0.35, relheight=0.4)

		# Add popup menu code, binding the right-click to selected text only
		self.popup_menu = tk.Menu(self, tearoff=0, background='#1c1b1a',
								  fg='white', activebackground='#534c5c',
                             	  activeforeground='Yellow')
		self.txt1.tag_bind("sel", '<Button-3>', self.popup)


		# This text box below user input box stores. It stores original input
		mylabel2 = tk.Label(self.frame,text= "Original Input:", bg='#AFAFAF',
							fg="black",font="none 10 normal")
		mylabel2.place(relx=0.1, rely=0.51)
		self.txt2 = scrolledtext.ScrolledText(self.frame,bg="white", width=50,font="Arial 10")
		self.txt2.pack(expand=True, fill='both')
		self.txt2.place(relx=0.1, rely= 0.55, relwidth=0.35, relheight=0.4)

		# This is the submit button
		Button1 = ttk.Button(self.frame, text="SUBMIT", width=7, command=self.Submit)
		Button1.place(relx=0.37, rely=0.05)


		# This says "Dictionary:" on top of the dictionary box
		VwDict = tk.Label(self.frame, text="Dictionary:", bg='#AFAFAF',
							fg="black",font="none 10 normal")
		VwDict.place(relx=0.55, rely=0.05)

		# This is the search box below the dictionary
		self.user_search = tk.StringVar()
		searchbox = tk.Entry(self.frame, textvariable=self.user_search)
		searchbox.place(relx=0.55, rely=0.52, relwidth=0.23)

		Button2 = ttk.Button(self.frame, text="SEARCH", width=9, command=self.Search)
		Button2.place(relx=0.80, rely=0.515)


		# This is the box containing all the Valid Words in the Dictionary (VwDict)
		self.VwDictList = tk.Listbox(self.frame, bg= '#FFFFFF', fg="black", font="none 10 normal")
								
		for word in self.dictionary:
			self.VwDictList.insert(tk.END, word)

		# Scrollbar should be attached to `VwDictList`
		VwScrollBar = tk.Scrollbar(self.VwDictList, orient = tk.VERTICAL)
		VwScrollBar.config(command = self.VwDictList.yview)
		VwScrollBar.pack(side=tk.RIGHT, fill = tk.Y)

		# Placing the dictionary list
		self.VwDictList.pack(expand=True, fill='both')
		self.VwDictList.config(yscrollcommand = VwScrollBar.set)
		self.VwDictList.place(relx=0.55, rely=0.1, relwidth=0.35, relheight=0.4)


		# Writing instructions on bottom right
		inst1 = tk.Label(self.frame, text = "Instructions for use:", anchor = 'w',
						 fg="black", font="none 10 bold")
		inst1.place(relx=0.55, rely=0.6, relwidth=0.37)
		inst2 = tk.Label(self.frame, text = "1. Enter text in the given area.",
						 anchor = 'w')
		inst2.place(relx=0.55, rely=0.63, relwidth=0.37)
		inst3 = tk.Label(self.frame, text = "2. Press the SUBMIT button.",
						 anchor = 'w')
		inst3.place(relx=0.55, rely=0.66, relwidth=0.37)
		inst4 = tk.Label(self.frame, text = "3. Double-click a highlighted word to select it.",
						 anchor = 'w')
		inst4.place(relx=0.55, rely=0.69, relwidth=0.37)
		inst5 = tk.Label(self.frame, text = "4. Right-click the selected error word.",
						 anchor = 'w')
		inst5.place(relx=0.55, rely=0.72, relwidth=0.37)
		inst6 = tk.Label(self.frame, text = "5. Choose one candidate correction word,",
						 anchor = 'w')
		inst6.place(relx=0.55, rely=0.75, relwidth=0.37)
		inst7 = tk.Label(self.frame, text = "    or add the selected word to dictionary.",
						 anchor = 'w')
		inst7.place(relx=0.55, rely=0.78, relwidth=0.37)


	def make_bigram_model(self):

		model_bl = {}
		for key, value in zip(self.counts_bl.keys(), self.counts_bl.values()):
			model_bl[key] = value / self.counts_u[key[0]]

		model_br = {}
		for key, value in zip(self.counts_br.keys(), self.counts_br.values()):
			model_br[key] = value / self.counts_u[key[0]]

		return model_bl, model_br


	def make_trigram_model(self):

		model_t = {}
		for key, value in zip(self.counts_t.keys(), self.counts_t.values()):
			model_t[key] = value / ((self.counts_bl[key[:2]] + self.counts_br[key[-1:-3:-1]]) / 2)

		return model_t


	def text_selected(self):
		if self.non_words:
			self.selection_ind = self.txt1.tag_ranges(tk.SEL)
			if self.selection_ind:
				return True
			else:
				return False
		else:
			return False


	def popup(self, event):
		
		if self.text_selected():
			selected = self.txt1.get(*self.selection_ind)
			
			if selected in self.non_words:
				try:	

					nd = len(self.candidate_words(selected))
					self.popup_menu.delete(0, nd+3)

					c = self.candidate_words(selected)

					if nd == 0:
						self.popup_menu.add_command(label = "No suggestions.")
						print("No suggestions.")

					if nd > 0:
						self.popup_menu.add_command(label = f"{c[0][1]} | {c[0][0]}",
							command = lambda: self.choose_correction(c[0][0]))
						self.popup_menu.add_separator()
					# using `for` loops here makes it buggy - the last word is chosen 
					# instead of the one that is clicked. 
					# forced to write inefficient code here

					#for i in range(1,nd):
					#	self.popup_menu.add_command(label = f"{c[i][1]} | {c[i][0]}",
					#		command = lambda: self.choose_correction(f"{c[i][0]}"))
					#for ccw in c[1:]:
					#	self.popup_menu.add_command(label = f"{ccw[1]} | {ccw[0]}",
					#		command = lambda: choose_correction(ccw[0]))
					if nd > 1:
						self.popup_menu.add_command(label = f"{c[1][1]} | {c[1][0]}",
							command = lambda: self.choose_correction(c[1][0]))
					if nd > 2:
						self.popup_menu.add_command(label = f"{c[2][1]} | {c[2][0]}",
							command = lambda: self.choose_correction(c[2][0]))
					if nd > 3:
						self.popup_menu.add_command(label = f"{c[3][1]} | {c[3][0]}",
							command = lambda: self.choose_correction(c[3][0]))
					if nd > 4:
						self.popup_menu.add_command(label = f"{c[4][1]} | {c[4][0]}",
							command = lambda: self.choose_correction(c[4][0]))
					if nd > 0:
						self.popup_menu.add_separator()
						self.popup_menu.add_command(label = "Add to dictionary", 
							command = lambda: self.add_to_dict(selected))

					self.popup_menu.tk_popup(event.x_root, event.y_root)
				finally:
					self.popup_menu.grab_release()



			else:
				pass
		else:
			pass


	def Submit(self):
		"""
		This function is what happens when user clicks on the `SUBMIT` button.
		What happens? The application checks for non-word spelling errors.
		Should extend this so that application checks for non-words errors first, 
		then proceed to check for real-word errors.
		"""
		self.non_words = []
		self.txt2.configure(state = 'normal')
		self.txt2.delete('1.0', tk.END)

		# get the user input (ui)
		user_input = self.txt1.get('1.0', 'end-1c')

		ui = user_input
		ui.replace("?", ".")
		ui.replace("!", '.')
		sent_list = ui.split('.')

		for i in range(len(sent_list)):
			sent_list[i] = sent_list[i].lower()
			sent_list[i] = 'OSO ' + sent_list[i] + ' OEO'

		ui = ' '.join(sent_list)
		ui = re.sub('\s+', ' ', ui)
		ui = regexp_tokenize(ui, "[\w']+")

		#ui = regexp_tokenize(user_input.lower(), "[\w']+")

		# make unigrams, bigrams and trigrams out of user input
		uni = [w for w in ui if not w.isdigit()]
		bl = list(ngrams(uni, 2))
		br = [(w1,w2) for (w1,w2) in zip(uni[1:],uni[:-1])]
		tri = list(ngrams(uni, 3))

		# make bigrams and trigrams out of corpus
		left_bi, right_bi = self.make_bigram_model()
		tri_model = self.make_trigram_model()

		utext = ' '.join(uni)

		score_list = [] # this is the score list for real-word errors
		for t in tri:
			# non-word spellchecking
			if t[1] not in self.dictionary:
				self.non_words.append(t[1])
				
		
		# real-word spellchecking
		# only occurs if there are no non-word errors
		# uses Stupid Backoff with weighted scoring on trigrams,
		# left bigrams, and right bigrams
		if not self.non_words:
			for t in tri:
				d = 0.4    # backoff discount
				ll = 0.25  # weighting on left bigram
				lt = 0.5   # weighting on trigram
				lr = 0.25  # weighting on right bigram
				thresh = 6e-5  # threshold score to be considered a real-word error
					
				if t in tri_model:
					p_t = tri_model[t]
				elif ((t[:2] in left_bi) and (t[-1:-3:-1] in right_bi)):
					p_t = (d/2)*(left_bi[t[:2]] + right_bi[t[-1:-3:-1]])
				elif (t[:2] in left_bi):
					p_t = d*left_bi[t[:2]]
				elif (t[-1:-3:-1] in right_bi):
					p_t = d*right_bi[t[-1:-3:-1]]
				else:
					p_t = d*d*self.model_u[t[1]]

				if t[:2] in left_bi:
					p_bl = left_bi[t[:2]]
				else:
					p_bl = d*self.model_u[t[1]]

				if t[-1:-3:-1] in right_bi:
					p_br = right_bi[t[-1:-3:-1]]
				else:
					p_br = d*self.model_u[t[1]]

				score = ll*p_bl + lt*p_t + lr*p_br
				score = round(score, 3 - int(math.floor(math.log10(abs(score)))) - 1)
				score_list.append(score)
				if score < thresh:
					self.non_words.append(t[1])
				
		
		# https://stackoverflow.com/questions/24819123/how-to-get-the
		# -index-of-word-being-searched-in-tkinter-text-box
		# code from above website
		self.txt1.tag_config("red_tag", foreground = "red")
		for err in self.non_words:
			offset = '+%dc' % len(err)
			pos_start = self.txt1.search(err, '1.0', tk.END)
			while pos_start:
				pos_end = pos_start + offset
				self.txt1.tag_add("red_tag", pos_start, pos_end)
				pos_start = self.txt1.search(err, pos_end, tk.END)
		
		self.txt2.insert(tk.INSERT, user_input)
		self.txt2.configure(state = 'disabled')

		if not self.non_words:
			print(score_list)
			print("No non-word errors.\n")
		else:
			print(score_list)
			print('\n')

		return self.non_words


	def Search(self):
		""" """
		us = self.user_search.get()
		if us in self.dictionary:
			ind = self.dictionary.index(us)
			self.VwDictList.selection_set(ind)
			self.VwDictList.see(ind)
		else:
			pass


	def dl_distance(self, s1, s2):
		"""
		DEE-ELL distance, not DEE-EYE distance. 
		Stands for Damerau-Levenshtein edit distance.
		"""
		d = {}
		lenstr1 = len(s1)
		lenstr2 = len(s2)
		for i in range(-1,lenstr1+1):
			d[(i,-1)] = i+1
		for j in range(-1,lenstr2+1):
			d[(-1,j)] = j+1

		for i in range(lenstr1):
			for j in range(lenstr2):
				if s1[i] == s2[j]:
					cost = 0
				else:
					cost = 1
				d[(i,j)] = min(
							   d[(i-1,j)] + 1, # deletion
							   d[(i,j-1)] + 1, # insertion
							   d[(i-1,j-1)] + cost, # substitution
							  )
				if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
					d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

		return d[lenstr1-1,lenstr2-1]


	def candidate_words(self, error):

		# create empty lists so that we can store our generated candidate words
		dist_one = []
		dist_two = []
		dist_three = []

		# for each word in the dictionary, calculate the DL distance between
		# that word and the error
		for word in self.dictionary:
			if word not in ['OEO','OSO']:
				# this `d` is the DL distance between word and error
				d = self.dl_distance(error, word)

				# if distance is 1, put that word into the dist_one list, and so on
				# but we also group up that word with its DL distance and its 
				# unigram probability, as calculated from the unigram model
				# only up to edit distance 3 self.model_u
				if d == 1: 
					dist_one.append((word, d, self.model_u[word]))
				elif d == 2:
					dist_two.append((word, d, self.model_u[word]))
				elif d == 3:
					dist_three.append((word, d, self.model_u[word]))
				else:
					pass

		# this is the key to which we sort the elements in the candidate word lists
		def sort_by_prob(element):
			return element[2]

		# here, we sort candidate words according to how likely they are 
		# to appear in the corpus, according to unigram language model
		dist_one = sorted(dist_one, key = sort_by_prob, reverse = True)
		dist_two = sorted(dist_two, key = sort_by_prob, reverse = True)
		dist_three = sorted(dist_three, key = sort_by_prob, reverse = True)

		# concatenate the three lists together and get the first 5 most 
		# probable candidate corrections
		candidates = dist_one + dist_two + dist_three

		return candidates[:5]


	def add_to_dict(self, word):

		if word.isalpha():
			self.dictionary.append(word)
			self.unigrams.append(word)
			self.counts_u[word] = 1
			self.model_u[word] = 1/len(self.dictionary)
			self.VwDictList.insert(tk.END, word)

			with io.open("dictionary.txt", "a", encoding = "utf-16") as f:
				f.write(f"\n{word}")
			with io.open("clean_economics.txt", "a", encoding = "utf-16") as f:
				f.write(f" {word}")

			print("Successfully added word to dictionary.")
		else:
			print("Select only the word, without punctuation or space.")


	def choose_correction(self, correction):
		self.txt1.delete(*self.selection_ind)
		self.txt1.insert(tk.INSERT, correction)


if __name__ == "__main__":
	sgui = SpellcheckerGUI()
	sgui.mainloop()