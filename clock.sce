
scenario = "clock";
response_matching = simple_matching;

##### 1) header parameter section ##### ##### 

# basic screen settings
default_font_size = 15; 
default_font = "Verdana";
default_background_color = 204,204,204; # light grey
default_text_color = 0,0,0; # black

# button definition 
active_buttons = 2;
button_codes = 1,2;

##### SDL section ##### ##### 
begin;

array { ### holds instructions and text elements
	picture{text{text_align = align_left; caption = #1
		"In this task, you will see a clock with a rotating timer on the computer screen. \n
		You will be required to make time judgements using this clock. Sometimes you will \n
		be asked to judge the time at which you pressed a button. On other occasions you  \n
		will have to judge the time at which you heard a tone. It is important that you   \n
		simply use an instinctive judgement for your estimates – do not think of a pre-decided \n
		clock time and do not try to use a planned strategy for the judgements.\n \n
		For further instructions press 'Enter'...";  };x = 0; y = 0;};

	picture{text{caption = " ";};x = 0 ; y = 0;};#2
		
	picture{text{text_align = align_left; caption = #3
		"Now we will begin the task. The following instructions will explain what you need \n
		to do for the first part of the task. Ask the experimenter if you are not sure what \n
		to do at any time. Please now put on the headphones. Press 'Enter' to continue...";};x = 0 ; y = 0;}; 
	
	picture{text{text_align = align_left; caption = #4
		"Condition A\n\n
		In this part of the task, you are to press the left mouse button with your right \n
		index finger at a random moment of your choosing, and this will produce a tone.  \n
		Each time, the experimenter will then ask you to report the position that the    \n
		clock hand was in WHEN YOU PRESSED THE BUTTON. Remember not to press the button \n
		at a predecided time, just do so at a random point.";};x = 0; y = 0;}; 
		
	picture{text{text_align = align_left; caption = #5
		"Condition B\n\n
		In this part of the task, press the left mouse button with your right index \n
		finger at a random moment of your choosing, and this will produce a tone.    \n
		Each time, the experimenter will then ask you to report the position that the \n
		clock hand was in WHEN YOU HEARD THE TONE. Remember not to press the button \n
		at a predecided time, just do so at a random point.";};x = 0; y = 0;};

	picture{text{text_align = align_left; caption = #6
		"Condition C\n\n
		In this part of the task, you are to press the left mouse button with your right \n
		index finger at a random moment of your choosing. You will not hear any tone. After \n
		each press, the experimenter will then ask you to report the position that the clock\n
		hand was in WHEN YOU PRESSED THE BUTTON. Remember not to press the button \n
		at a predecided time, just do so at a random point.";};x = 0; y = 0;}; 
		
	picture{text{text_align = align_left; caption = #7
		"Condition D\n\n
		In this part of the task, you do not need to press any button. \n
		You will simply wait until you hear a tone, and after each time, the \n 
		experimenter will ask you to report the position that the clock hand was in \n 
		WHEN YOU HEARD THE TONE.";};x = 0; y = 0;}; 
		
	picture{text{caption = #8
		"This is the end of the computer tasks. Thank you very much for taking part!";};x = 0; y = 0;}; 
} instructions;

# stimulus definition
# clock hand 
line_graphic{}hand;

# basic template: sounds
sound { wavefile { preload = false; } wave; } snd;

### trial definitions
# presentation of clock rotation
trial{
	trial_duration = 16;
	monitor_sounds = false;
	stimulus_event {
		sound snd;
	}tone;
		
	stimulus_event {
		picture{  
			ellipse_graphic { # black edge of the clock face 
				ellipse_width = 220;
				ellipse_height = 220;
				color = 0, 0, 0;
				rotation = 30;
			}circle_edge; 
			x = 0; y = 0;
			
			ellipse_graphic {# grey inner part of the clock face 
				ellipse_width = 209;
				ellipse_height = 209;
				color = 204, 204, 204;
				rotation = 30;
			}circle;
			x = 0; y = 0;
			
			text{caption = " ";}instruction2a; x = 0; y = 275;
			text{caption = " ";}instruction2b; x = 0; y = -275;
			
			text{caption = "5";}; x = 65; y = 112;
			text{caption = "10";}; x = 112; y = 65;
			text{caption = "15";}; x = 130; y = 0;
			 
			text{caption = "20";}; x = 112; y = -65;
			text{caption = "25";}; x = 65; y = -112;
			text{caption = "30";}; x = 0; y = -130;
			
			text{caption = "35";}; x = -65; y = -112;
			text{caption = "40";}; x = -112; y = -65;
			text{caption = "45";}; x = -130; y = 0;
			
			text{caption = "50";}; x = -112; y = 65;
			text{caption = "55";}; x = -65; y = 112;
			text{caption = "60";}; x = 0; y = 130;
			
		}clock_pic;
		duration = next_picture;
	}clock_face; 
}clock_trial;

# presentation of empty screen
trial{
	trial_type = specific_response;
	trial_duration = forever;
	terminator_button = 2;
	picture{};
}empty;

# presentation of empty screen
trial{
	trial_duration = 20;
	stimulus_event{
		picture{};
		code = "report";
	}report_event;
}report;

# presentation of one instruction
trial{
	trial_type = specific_response; 
	terminator_button = 1,2;	
	trial_duration = forever; # ... trial ends if and only if button 4 ('Enter') or 3 ('Backspace') is pressed
	stimulus_event {
		picture{ text{caption = " ";}; x = 0; y = 0;};
		code = "instruction";
	}texts; 
}instruction;

##### PCL-section ##### #####
begin_pcl;

### BASIC SETTINGS ###

# number of trials per condition
int number_trials = 20;

# set clock hand parameter and add clock hand to clock face 
hand.set_next_line_width(5.0);
hand.set_line_color(0,0,0,255);
clock_pic.add_part(hand, 0.0, 0.0);

# parameter for calculation of the clock hand's position
double conversion = (pi_value*2.0)/2560.0; 
double end_x;
double end_y;

# time parameter
int time_zero = 0;
int time = 0;
int time_end_part1 = 0;
int time_end_part2 = 0;
int tone_delay = 0;

# send commands to AudioSpace to construct sound data in channels
audio_space.run( "channel0 = 0.5 * silence(10, 0)" );
audio_space.run( "channel1 = 0.5 * sin( 1000, 0, 75, 0 )" );
# construct sounds by combining channels
audio_space.run( "wave0 = (channel0, channel0)" );
audio_space.run( "wave1 = (channel1, channel1)" );

################
# SUB-ROUTINES #
################

### CLOCK ROTATES UNTIL BUTTON PRESS ###

sub clock_button
begin  
	# loop: present clock until button is pressed
	loop int last_button = 0; 
	until last_button == 1
	begin
		audio_space.get_wave_data("wave0", wave ); # import a sound from AudioSpace
		
		time = clock.time()- time_zero; # "time" == current duration of the trial (== current time - time_zero)
		
		# calculation of the clock hand's current position 
		double x = double((time % 2560));
		end_x = sin(x * conversion)*100.0;
		end_y = cos(x * conversion)*100.0;
		
		# draw clock hand at the current position, present trial and remove old clock hand 
		hand.add_line(0.0, 0.0, end_x, end_y); 
		
		#hand.set_next_line_width(4.0);
		
		loop int counter = 1
		until counter == 13
		begin
			end_x = sin(213.3*double(counter)*conversion);
			end_y = cos(213.3*double(counter)*conversion);
			hand.add_line( end_x*105.0,end_y*105.0, end_x*113.0,end_y*113.0);
			counter = counter+1;
		end;
		
		hand.redraw();
		clock_trial.present();
		hand.clear();
		
		# get keybord response 
		last_button = response_manager.last_response(); 
	end;
	time_end_part1 = time;	
end;

### CLOCK ROTATES - TONE IS PRESENTED ###
	
sub clock_tone
begin	
	# loop: present clock for a randomized amount of time - presentation of tone 250 ms after button press 
	loop bool tone_done = false;
	until time >= time_end_part1 + tone_delay + 75
	begin
		audio_space.get_wave_data("wave0", wave ); # import a sound from AudioSpace

		if (time >= time_end_part1 + tone_delay) && (tone_done == false) then # present auditive stimulus 250 ms after button press
			audio_space.get_wave_data("wave1", wave ); # import a sound from AudioSpace
			tone_done = true;
			end; 
		time = clock.time()- time_zero; # "time" == current duration of the trial (== current time - time_zero)
		
		# calculation of the clock hand's current position 
		double x = double((time % 2560));
		end_x = sin(x * conversion)*100.0;
		end_y = cos(x * conversion)*100.0;
		
		# draw clock hand at the current position, present trial and remove old clock hand 
		hand.add_line(0.0, 0.0, end_x, end_y); 
	
		#hand.set_next_line_width(4.0);
		
		loop int counter = 1
		until counter == 13
		begin
			end_x = sin(213.3*double(counter)*conversion);
			end_y = cos(213.3*double(counter)*conversion);
			hand.add_line( end_x*105.0,end_y*105.0, end_x*113.0,end_y*113.0);
			counter = counter+1;
		end;
		
		hand.redraw();
		clock_trial.present();
		hand.clear()
	end;
	time_end_part2 = time;
end;

### CLOCK CONTINUES ROTATING FOR A RANDOM AMOUNT OF TIME, STOPS AND DISAPPEARS ###

sub continue_running
begin
	int random_delay = int(random()*1000.0)+1425; # clock will stop rotation 1500-2500 ms after the tone was presented  
	
	# loop: present clock for a randomized amount of time - presentation of tone 250 ms after button press 
	loop
	until time > time_end_part2 + random_delay
	begin
		audio_space.get_wave_data("wave0", wave ); # import a sound from AudioSpace
		time = clock.time()- time_zero; # "time" == current duration of the trial (== current time - time_zero)
		
		#hand.set_next_line_width(4.0);
		
		loop int counter = 1
		until counter == 13
		begin
			end_x = sin(213.3*double(counter)*conversion);
			end_y = cos(213.3*double(counter)*conversion);
			hand.add_line( end_x*105.0,end_y*105.0, end_x*113.0,end_y*113.0);
			counter = counter+1;
		end;
		
		hand.set_next_line_width(5.0);
		
		# calculation of the clock hand's current position 
		double x = double((time % 2560));
		end_x = sin(x * conversion)*100.0;
		end_y = cos(x * conversion)*100.0;
		
		# draw clock hand at the current position, present trial and remove old clock hand 
		hand.add_line(0.0, 0.0, end_x, end_y); 
		
		hand.redraw();
		clock_trial.present();
		hand.clear()
	end;
	
	response_manager.set_button_active(2, true); # set 'Enter' active
	
	# present stopped clock until 'Enter' is pressed
	audio_space.get_wave_data("wave0", wave ); # import a sound from AudioSpace

	# draw clock hand at the current position, present trial and remove old clock hand 
	clock_trial.set_type(specific_response);
	clock_trial.set_duration(forever);
	clock_trial.set_terminator_button(2);	

	hand.add_line(0.0, 0.0, end_x,end_y);
	#hand.set_next_line_width(4.0);	
	loop int counter = 1
	until counter == 13
	begin
		end_x = sin(213.3*double(counter)*conversion);
		end_y = cos(213.3*double(counter)*conversion);
		hand.add_line( end_x*105.0,end_y*105.0, end_x*113.0,end_y*113.0);
		counter = counter+1;
	end;
	
	hand.redraw();
	clock_trial.present();
	hand.clear();

	clock_trial.set_type(fixed);
	clock_trial.set_duration(16);
		
	empty.present();
	
	response_manager.set_button_active(2, false); # set 'Enter' inactive 
	report.present();
	
end;

### DISPLAY INSTRUCTION

sub instruction (int block_number)
begin
	response_manager.set_button_active(1, false); # set mouse inactive
	response_manager.set_button_active(2, true); # set 'Enter' active
	texts.set_stimulus(instructions[block_number+3]); instruction.present(); 
	response_manager.set_button_active(2, false); # set 'Enter' inactive
	response_manager.set_button_active(1, true); # set mouse active
end;

##############
# EXPERIMENT #
##############

# display instructions
loop int page = 1
until page == 4
begin 
	if page == 2 then 
		instruction2a.set_caption("The clock you will use looks like this. \n\nWhen you make your time judgements, try to be as numerically accurate as you can.", true); 
		instruction2b.set_caption("The numbers on the clock face are just a guide – do not restrict yourself to only using those numbers. \n\nClick the mouse button to continue...", true); 
		clock_button();
		instruction2a.set_caption(" ", true);
		instruction2b.set_caption(" ", true);
		page = 3; end; 
	texts.set_stimulus(instructions[page]); instruction.present(); 
	int last_button = response_manager.last_response(); # get keybord response 
	if last_button == 1 then page = 1; # go back to last page following 'Backspace' press
	elseif last_button == 2 then page = page+1; end; # go to next page following 'Enter' press
	if page < 1 then page = 1; end; # can't go back from 1st page
end;

response_manager.set_button_active(2, false); # set 'Enter' inactive

array <int> randomisation[4] = {1,2,3,4}; # array used for randomisation
randomisation.shuffle();

#loop int h = 0 until h == 5 begin
	randomisation.shuffle();
	#term.print(string(randomisation[1]) + "\n" + string(randomisation[2]) + "\n" +string(randomisation[3]) + "\n" +string(randomisation[4]) + "\n");
	#h = h + 1;
#end;

loop int count_blocks = 1
until count_blocks == 5
begin 
	int which = randomisation[count_blocks];
	if which == 1 then  # agency condition #
		term.print("\n\nCondition A\n");
		instruction(which);
		loop int count = 0
		until count == number_trials
		begin
			#term.print("\ntrial no " + string(count+1));
			tone_delay = 250;
			time_zero = clock.time(); # save time of the trials start as "time_zero"
			#term.print("\nAgency Condition time_zero" + string(time_zero) + " time " + string(time) + " time_end_part1 " + string(time_end_part1) + " time_end_part2 " + string(time_end_part2)); # debugging structure 
			clock_button();
			report_event.set_event_code("\nReportA" + " \t" + string(round(((double(time_end_part1%2560)/2560.0)*60.0),2)) + " \t" + string(round(((double(time_end_part1)/2560.0)*60.0),2)));
			clock_tone();
			continue_running();
			count = count +1;
		end;

	elseif which == 2 then	# agency condition # 
		term.print("\n\nCondition B\n");
		instruction(which);
		
		loop int count1 = 0
		until count1 == number_trials
		begin
			#term.print("\ntrial no " + string(count1+1));
			tone_delay = 250;
			time_zero = clock.time(); # save time of the trials start as "time_zero"
			time = clock.time()- time_zero; time_end_part1 = 0; time_end_part2 = 0; 
			clock_button();
			report_event.set_event_code("\nReportB" + " \t" + string(round(((double(time_end_part1%2560)/2560.0)*60.0),2)) + " \t" + string(round(((double(time_end_part1)/2560.0)*60.0),2)));
			clock_tone();
			continue_running();
			count1 = count1 +1;
		end;

	elseif which == 3 then	# baseline action 
		term.print("\n\nCondition C\n");
		instruction(which);
	
		loop int count2 = 0
		until count2 == number_trials
		begin
			#term.print("\ntrial no " + string(count2+1));
			tone_delay = 250;
			time_zero = clock.time(); # save time of the trials start as "time_zero"
			time = clock.time()- time_zero; time_end_part1 = 0; time_end_part2 = 0; 
			clock_button();
			report_event.set_event_code("\nReportC" + " \t" + string(round(((double(time_end_part1%2560)/2560.0)*60.0),2)) + " \t" + string(round(((double(time_end_part1)/2560.0)*60.0),2)));
			time_end_part2 = time_end_part1;
			continue_running();
		count2 = count2 +1;
		end;

	elseif which == 4 then # baseline tone 
		term.print("\n\nCondition D\n");
		instruction(which);

		loop int count3 = 0
		until count3 == number_trials
		begin
			#term.print("\ntrial no " + string(count3+1));
			tone_delay = int(random()*2560.0)+2560;
			report_event.set_event_code("\nReportD" + " \t" + string(round(((double(tone_delay%2560)/2560.0)*60.0),2)) + " \t" + string(round(((double(tone_delay)/2560.0)*60.0),2)));

			time_zero = clock.time(); # save time of the trials start as "time_zero"
			time = clock.time()- time_zero; time_end_part1 = 0; time_end_part2 = 0; 
			clock_tone();
			continue_running();
		count3 = count3 +1;
		end;
	end;
	count_blocks = count_blocks+1;
end;

instruction(5);