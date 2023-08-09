import gradio as gr
import time
import os
from difflib import SequenceMatcher
from functions import voice2text, text2voice, clean_text, open_data, update_data

# -----

def gen_progress(dictionary, target_score):
    value = {}
    completed = 0
    for i in dictionary:
        if dictionary[i] >= target_score:
            completed = completed + 1
        else:
            value[i] = dictionary[i] / target_score
    
    value[f"✅ {lang['total'][l]}"] = completed / len(dictionary)

    return value

def reload(user_update):
    global user, user_config, member_config, l, lang, dic
    user = user_update

    user_config = open_data(f"users/{user}.yaml")
    member_config = open_data(f"users/{user}.yaml")
    l = user_config['language']
    lang = open_data('lang.yaml')
    dic = open_data('dic.yaml')

    update_data(f"users/{user}.yaml", user_config)

    if user == '100000':
        # Tabs
        account_acc = gr.Accordion.update(label=lang['Account settings'][l], visible=False)
        teacher_s_acc = gr.Accordion.update(label=lang['Teacher settings'][l], visible=False)
        teacher_rs_acc = gr.Accordion.update(label=lang['Read and speak'][l], visible=False)
        rs_acc = gr.Accordion.update(label=lang["Read and speak"][l])

        # Home
        login_user = gr.Textbox.update(label=lang['Your ID'][l], visible=True)
        login_pass = gr.Textbox.update(label=lang['Password'][l], visible=True)
        login_button = gr.Button.update(value=lang['Login'][l], visible=True)
        logout_button = gr.Button.update(value=lang['Logout'][l], visible=False)
        user_id = gr.Markdown.update(value=f"{lang['Your ID'][l]}: {user}", visible=False)
    else:
        # Tabs
        account_acc = gr.Accordion.update(label=lang['Account settings'][l], visible=True)
        teacher_s_acc = gr.Accordion.update(label=lang['Teacher settings'][l], visible=True)
        teacher_rs_acc = gr.Accordion.update(label=lang['Read and speak'][l], visible=True)
        rs_acc = gr.Accordion.update(label=lang["Read and speak"][l])

        # Home
        login_user = gr.Textbox.update(label=lang['Your ID'][l], visible=False)
        login_pass = gr.Textbox.update(label=lang['Password'][l], visible=False)
        login_button = gr.Button.update(value=lang['Login'][l], visible=False)
        logout_button = gr.Button.update(value=lang['Logout'][l], visible=True)
        user_id = gr.Markdown.update(value=f"{lang['Your ID'][l]}: {user}", visible=True)

    # General
    reload_button = gr.Button.update(value=lang['Reload'][l])
    cancel_button = gr.Button.update(value=lang['Cancel'][l])

    # Home
    user_welcome = gr.Markdown.update(value=f"# {lang['Welcome'][l]} {user_config['name']}!")
    user_lang = gr.Dropdown.update(value=l, visible=True)

    # Account settings
    user_name = gr.Textbox.update(label=lang['Name'][l], value=user_config['name'])
    user_pass = gr.Textbox.update(label=lang['Password'][l])
    user_pass2 = gr.Textbox.update(label=lang['Repeat password'][l])
    save_us_button = gr.Button.update(value=lang['Save'][l])
    user_credentials = gr.Markdown.update(value=f"### {lang['Credentials'][l]}")
    save_cred_button = gr.Button.update(value=lang['Save'][l])
    user_settings = gr.Markdown.update(value=f"### {lang['Members'][l]}")
    add_button = gr.Button.update(value=lang['Add'][l])
    del_button = gr.Button.update(lang['Delete member'][l])
    members = gr.Dropdown.update(value=user)

    # Teacher settings
    teacher_settings_user = gr.Dropdown.update(value=user, choices=list(user_config['members'].keys()))

    v2t_model = gr.Dropdown.update(label=lang['Voice to text model'][l], value=user_config['teacher']['read_speak']['v2t'], choices=dic['v2t'])
    t2v_model = gr.Dropdown.update(value='gTTS')
    new_rs_voice = gr.Dropdown.update(value='Default')
    voice_speed = gr.Slider.update(label=lang['Voice speed'][l], value=user_config['teacher']['read_speak']['speed'], minimum=0.5, maximum=1.0)
    teacher_rs_ex = gr.Number.update(label=lang['Exchange rate'][l], value=user_config['teacher']['read_speak']['rate'])
    target_score = gr.Number.update(label=lang['Target score'][l], value=user_config['teacher']['read_speak']['target_score'])
    difficulty = gr.Slider.update(label=lang["Difficulty"][l], value=user_config['teacher']['read_speak']['difficulty'], minimum=1.0, maximum=5.0)

    new_rs = gr.Textbox.update(placeholder=lang['New homework'][l])
    new_rs_button = gr.Button.update(lang['New homework'][l])
    rs_hw_df = gr.Dataframe.update()
    save_rs_button = gr.Button.update(lang['Save'][l])
    del_rs_button = gr.Button.update(lang['Delete homework'][l])

    # Teacher
    balance_text = gr.Markdown.update(value=f"{lang['Your balance'][l]}: $ {round(user_config['teacher']['balance'], 2)}")
    rs = gr.Radio.update(choices=list(user_config['teacher']['read_speak']['homeworks'].keys()))
    rs_hw = gr.Dropdown.update(label=lang['Select homework'][l])
    audio_example = gr.Audio.update(label=lang['Listen to this'][l])
    button_send = gr.Button.update(value=lang['Send'][l])

    return reload_button, cancel_button,  account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_id, user_lang, login_user, login_pass, login_button, logout_button, user_name, user_pass, user_pass2, save_us_button, user_credentials, save_cred_button, user_settings, add_button, del_button, members, teacher_settings_user, v2t_model, t2v_model, new_rs_voice, voice_speed, teacher_rs_ex, target_score, difficulty, new_rs, new_rs_button, rs_hw_df, save_rs_button, del_rs_button, balance_text, rs_hw, rs, audio_example, button_send

def no_change():
    account_acc = gr.Accordion.update()
    teacher_s_acc = gr.Accordion.update()
    teacher_rs_acc = gr.Accordion.update()
    rs_acc = gr.Accordion.update()

    # Home
    login_user = gr.Textbox.update()
    login_pass = gr.Textbox.update()
    login_button = gr.Button.update()
    logout_button = gr.Button.update()
    user_id = gr.Markdown.update()

    # General
    reload_button = gr.Button.update()
    cancel_button = gr.Button.update()

    # Home
    user_welcome = gr.Markdown.update()
    user_lang = gr.Dropdown.update()

    # Account settings
    user_name = gr.Textbox.update()
    user_pass = gr.Textbox.update()
    user_pass2 = gr.Textbox.update()
    save_us_button = gr.Button.update()
    user_credentials = gr.Markdown.update()
    save_cred_button = gr.Button.update()
    user_settings = gr.Markdown.update()
    add_button = gr.Button.update()
    del_button = gr.Button.update()
    members = gr.Dropdown.update()

    # Teacher settings
    teacher_settings_user = gr.Dropdown.update()

    v2t_model = gr.Dropdown.update()
    t2v_model = gr.Dropdown.update()
    new_rs_voice = gr.Dropdown.update()
    voice_speed = gr.Slider.update()
    teacher_rs_ex = gr.Number.update()
    target_score = gr.Number.update()
    difficulty = gr.Slider.update()

    new_rs = gr.Textbox.update()
    new_rs_button = gr.Button.update()
    rs_hw_df = gr.Dataframe.update()
    save_rs_button = gr.Button.update()
    del_rs_button = gr.Button.update()

    # Teacher
    balance_text = gr.Markdown.update()
    rs = gr.Radio.update()
    rs_hw = gr.Dropdown.update()
    audio_example = gr.Audio.update()
    button_send = gr.Button.update()

    return reload_button, cancel_button,  account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_id, user_lang, login_user, login_pass, login_button, logout_button, user_name, user_pass, user_pass2, save_us_button, user_credentials, save_cred_button, user_settings, add_button, del_button, members, teacher_settings_user, v2t_model, t2v_model, new_rs_voice, voice_speed, teacher_rs_ex, target_score, difficulty, new_rs, new_rs_button, rs_hw_df, save_rs_button, del_rs_button, balance_text, rs_hw, rs, audio_example, button_send

def cancel_button_change():
    gr.Warning('Cancelled ...')

# -----

def reload_button_change():
    global user
    return reload(user)

def user_lang_change(user_lang_n):
    global user, l

    user_config = open_data(f'users/{user}.yaml')
    user_config['language'] = user_lang_n
    update_data(f'users/{user}.yaml', user_config)
    return reload(user)

def login_button_change(login_user_n, login_pass_n):
    time.sleep(1)
    if os.path.exists('users/'+login_user_n+'.yaml'):
        r_pass = open_data(f"users/{login_user_n}.yaml")['pass']
        if r_pass == login_pass_n:
            global user
            user = login_user_n
            return reload(user)
        else:
            gr.Warning("Dont you remember your credentials?")
            return no_change()
    else:
        gr.Warning("Who you are!?")
        return no_change()

def logout_button_change():
    global user, user_config, member_config, l, lang, dic

    user = '100000'
    user_config = open_data(f"users/{user}.yaml")
    member_config = open_data(f"users/{user}.yaml")
    l = user_config['language']
    lang = open_data('lang.yaml')
    dic = open_data('dic.yaml')

    update_data(f"users/{user}.yaml", user_config)

    # Tabs
    account_acc = gr.Accordion.update(label=lang['Account settings'][l], visible=False)
    teacher_s_acc = gr.Accordion.update(label=lang['Teacher settings'][l], visible=False)
    teacher_rs_acc = gr.Accordion.update(label=lang['Read and speak'][l], visible=False)
    rs_acc = gr.Accordion.update(label=lang["Read and speak"][l])

    # Home
    login_user = gr.Textbox.update(label=lang['Your ID'][l], visible=True)
    login_pass = gr.Textbox.update(label=lang['Password'][l], visible=True)
    login_button = gr.Button.update(value=lang['Login'][l], visible=True)
    logout_button = gr.Button.update(value=lang['Logout'][l], visible=False)
    user_id = gr.Markdown.update(value=f"{lang['Your ID'][l]}: {user}", visible=False)
    user_welcome = gr.Markdown.update(value=f"# {lang['Welcome'][l]} {user_config['name']}!")
    user_lang = gr.Dropdown.update(visible=False)

    # Teacher
    balance_text = gr.Markdown.update(value=f"{lang['Your balance'][l]}: $ {round(user_config['teacher']['balance'], 2)}")
    rs = gr.Radio.update(choices=list(user_config['teacher']['read_speak']['homeworks'].keys()))
    rs_hw = gr.Dropdown.update(label=lang['Select homework'][l])
    audio_example = gr.Audio.update(label=lang['Listen to this'][l])
    button_send = gr.Button.update(value=lang['Send'][l])

    return account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_lang, user_id, login_user, login_pass, login_button, logout_button, balance_text, rs_hw, rs, audio_example, button_send

def save_us_button_change(user_name, user_pass, user_pass2):
    global user_config

    if user == '000000':
        raise gr.Error(lang['Create an account first'][l])
    else:
        if user_pass == user_pass2:
            user_config = open_data(f"users/{user}.yaml")
            user_config['name'] = user_name
            user_config['pass'] = user_pass
            update_data(f"users/{user}.yaml", user_config)
        else:
            raise gr.Error(lang['Passwords do not match'][l])
    return gr.Markdown.update(value=f"# {lang['Welcome'][l]} {user_config['name']}!")

def add_button_change(member_add_id):
    members = gr.Dropdown.update()

    if os.path.exists(f"users/{member_add_id}.yaml"):
        if member_add_id != user:
            global user_config
            user_config = open_data(f"users/{user}.yaml")
            member0_config = open_data(f"users/{member_add_id}.yaml")

            user_config['members'][member_add_id] = True
            update_data(f"users/{user}.yaml", user_config)
            member0_config['withhold'].append(user)
            update_data(f"users/{member_add_id}.yaml", member0_config)

            members = gr.Dropdown.update(value=member_add_id, choices=list(user_config['members'].keys()))

    return members, members

def del_button_change(members):
    if members == user:
        return gr.Dropdown.update(), gr.Dropdown.update()
    else:
        global user_config

        user_config = open_data(f"users/{user}.yaml")
        member0_config = open_data(f"users/{members}.yaml")

        user_config['members'].pop(members)
        if user in member0_config['withhold']:
            member0_config['withhold'].remove(user)

        update_data(f"users/{user}.yaml", user_config)
        update_data(f"users/{members}.yaml", member0_config)

        teacher_settings_user = gr.Dropdown.update(choices=list(user_config['members'].keys()))

        return teacher_settings_user, teacher_settings_user

def save_cred_button_change(hf_token, openai_token, elevenlabs_token, azure_region, azure_token):
    global user_config

    user_config = open_data(f"users/{user}.yaml")
    user_config['credentials']['hf_token'] = hf_token
    user_config['credentials']['openai_token'] = openai_token
    user_config['credentials']['elevenlabs_token'] = elevenlabs_token
    user_config['credentials']['azure_region'] = azure_region
    user_config['credentials']['azure_token'] = azure_token
    update_data(f"users/{user}.yaml", user_config)

def teacher_settings_user_change(teacher_settings_user):
    global member_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")
    
    v2t_model = gr.Dropdown.update(value=member_config['teacher']['read_speak']['v2t'])
    voice_speed = gr.Slider.update(value=member_config['teacher']['read_speak']['speed'])
    teacher_rs_ex = gr.Number.update(value=member_config['teacher']['read_speak']['rate'])
    target_score = gr.Number.update(value=member_config['teacher']['read_speak']['target_score'])
    difficulty = gr.Slider.update(value=member_config['teacher']['read_speak']['difficulty'])
    if teacher_settings_user == user:
        expected_coins = gr.Markdown.update(visible=False)
    else:
        expected_coins = gr.Markdown.update(visible=True)

    new_rs = gr.Textbox.update(value='')
    current_rs = gr.Dropdown.update(value=None, choices=[i for i in list(member_config['teacher']['read_speak']['homeworks'].keys()) if member_config['teacher']['read_speak']['settings'][i]['by'] == user])
    new_rs_lang = gr.Dropdown.update(value='English')
    t2v_model = gr.Dropdown.update(value='gTTS')
    new_rs_voice = gr.Dropdown.update(value='Default')
    rs_hw_df = gr.Dataframe.update(value=None)

    return v2t_model, voice_speed, teacher_rs_ex, target_score, difficulty, expected_coins, new_rs, current_rs, new_rs_lang, t2v_model, new_rs_voice, rs_hw_df

def v2t_model_change(teacher_settings_user, v2t_model):
    global member_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")
    member_config['teacher']['read_speak']['v2t'] = v2t_model
    update_data(f"users/{teacher_settings_user}.yaml", member_config)

def new_rs_lang_change(new_rs_lang):
    if new_rs_lang == None:
        return gr.Dropdown.update(value=None, choices=None), gr.Dropdown.update(value=None, choices=None)
    else:
        t2v_model = gr.Dropdown.update(value='gTTS', choices=list(dic['languages'][new_rs_lang].keys()))
        new_rs_voice = gr.Dropdown.update(value=dic['languages'][new_rs_lang]['gTTS']['voices'][0], choices=dic['languages'][new_rs_lang]['gTTS']['voices'])
        return t2v_model, new_rs_voice

def t2v_model_change(new_rs_lang, t2v_model):
    if new_rs_lang == None or t2v_model == None:
        return gr.Dropdown.update(value=None, choices=None)
    else:
        new_rs_voice = gr.Dropdown.update(value=dic['languages'][new_rs_lang][t2v_model]['voices'][0], choices=dic['languages'][new_rs_lang][t2v_model]['voices'])
        return new_rs_voice

def voice_speed_change(teacher_settings_user, voice_speed):
    global member_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")
    member_config['teacher']['read_speak']['speed'] = voice_speed
    update_data(f"users/{teacher_settings_user}.yaml", member_config)

def teacher_rs_ex_change(teacher_settings_user, teacher_rs_ex, target_score):
    global member_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")
    member_config['teacher']['read_speak']['rate'] = teacher_rs_ex
    update_data(f"users/{teacher_settings_user}.yaml", member_config)

    return gr.Markdown.update(f"{lang['Expected coins'][l]}: $ {round(sum([1 for key in member_config['teacher']['read_speak']['homeworks'] for value in member_config['teacher']['read_speak']['homeworks'][key].values() if value % 1 == 0]) * target_score / teacher_rs_ex, 2)}")

def target_score_change(teacher_settings_user, target_score, teacher_rs_ex):
    global member_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")
    member_config['teacher']['read_speak']['target_score'] = target_score
    update_data(f"users/{teacher_settings_user}.yaml", member_config)

    return gr.Markdown.update(f"{lang['Expected coins'][l]}: $ {round(sum([1 for key in member_config['teacher']['read_speak']['homeworks'] for value in member_config['teacher']['read_speak']['homeworks'][key].values() if value % 1 == 0]) * target_score / teacher_rs_ex, 2)}")

def difficulty_change(teacher_settings_user, difficulty):
    global member_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")
    member_config['teacher']['read_speak']['difficulty'] = difficulty
    update_data(f"users/{teacher_settings_user}.yaml", member_config)

def current_rs_change(teacher_settings_user, current_rs):
    member_config = open_data(f"users/{teacher_settings_user}.yaml") 
    if current_rs == None:
        return gr.Dropdown.update(choices=list(dic['languages'].keys()), value=None), gr.Dataframe.update(value=None)
    else:
        return gr.Dropdown.update(choices=list(dic['languages'].keys()), value=member_config['teacher']['read_speak']['settings'][current_rs]['language']), gr.Dataframe.update(value=[[i, round(member_config['teacher']['read_speak']['homeworks'][current_rs][i], 2)] for i in list(member_config['teacher']['read_speak']['homeworks'][current_rs].keys())])

def new_rs_button_change(teacher_settings_user, new_rs):
    global member_config, user_config
    
    if teacher_settings_user != user:
         new_rs = f"{new_rs} [{user_config['name']}]"
    
    if new_rs not in list(member_config['teacher']['read_speak']['homeworks'].keys()):
        member_config = open_data(f"users/{teacher_settings_user}.yaml")

        member_config['teacher']['read_speak']['homeworks'][new_rs] = {}
        member_config['teacher']['read_speak']['homeworks'][new_rs]['example'] = 0
        member_config['teacher']['read_speak']['settings'][new_rs] = {}
        member_config['teacher']['read_speak']['settings'][new_rs]['language'] = 'English'
        member_config['teacher']['read_speak']['settings'][new_rs]['by'] = user
        member_config['teacher']['read_speak']['settings'][new_rs]['t2v'] = 'gTTS'
        member_config['teacher']['read_speak']['settings'][new_rs]['voice'] = 'Default'

        update_data(f"users/{teacher_settings_user}.yaml", member_config)
    
    current_rs = gr.Dropdown.update(choices=[i for i in list(member_config['teacher']['read_speak']['homeworks'].keys()) if member_config['teacher']['read_speak']['settings'][i]['by'] == user])
    
    user_config = open_data(f"users/{user}.yaml")
    rs = gr.Radio.update(choices=list(user_config['teacher']['read_speak']['homeworks'].keys()))

    return current_rs, rs

def save_rs_button_change(teacher_settings_user, current_rs, new_rs_lang, t2v_model, rs_hw_df, new_rs_voice, target_score, teacher_rs_ex):
    global member_config, user_config
    member_config = open_data(f"users/{teacher_settings_user}.yaml")

    hw = {}
    for i in rs_hw_df.index:
        if rs_hw_df.loc[i]['-'] != '':
            if rs_hw_df.loc[i]['Score'] == '':
                hw[rs_hw_df.loc[i]['-']] = 0.0
            else:
                try:
                    hw[rs_hw_df.loc[i]['-']] = int(rs_hw_df.loc[i]['Score'])
                except:
                    hw[rs_hw_df.loc[i]['-']] = 0.0

    member_config['teacher']['read_speak']['homeworks'][current_rs] = hw
    member_config['teacher']['read_speak']['settings'][current_rs] = {}
    member_config['teacher']['read_speak']['settings'][current_rs]['language'] = new_rs_lang
    member_config['teacher']['read_speak']['settings'][current_rs]['by'] = user
    member_config['teacher']['read_speak']['settings'][current_rs]['t2v'] = t2v_model
    member_config['teacher']['read_speak']['settings'][current_rs]['voice'] = new_rs_voice

    update_data(f"users/{teacher_settings_user}.yaml", member_config)

    expected_coins = gr.Markdown.update(f"{lang['Expected coins'][l]}: $ {round(sum([1 for key in member_config['teacher']['read_speak']['homeworks'] for value in member_config['teacher']['read_speak']['homeworks'][key].values() if value % 1 == 0]) * target_score / teacher_rs_ex, 2)}")

    user_config = open_data(f"users/{user}.yaml")
    return expected_coins, gr.Radio.update(choices=list(user_config['teacher']['read_speak']['homeworks'].keys()))

def del_rs_button_change(teacher_settings_user, current_rs, target_score, teacher_rs_ex):
    global member_config    
    member_config = open_data(f"users/{teacher_settings_user}.yaml")

    member_config['teacher']['read_speak']['homeworks'].pop(current_rs)
    member_config['teacher']['read_speak']['settings'].pop(current_rs)
    update_data(f"users/{teacher_settings_user}.yaml", member_config)

    current_rs = gr.Dropdown.update(choices=[i for i in list(member_config['teacher']['read_speak']['homeworks'].keys()) if member_config['teacher']['read_speak']['settings'][i]['by'] == user], value=None)
    rs_hw_df = gr.Dataframe.update(value=None)
    new_rs_lang = gr.Dropdown.update(value=None)
    expected_coins = gr.Markdown.update(f"{lang['Expected coins'][l]}: $ {round(sum([1 for key in member_config['teacher']['read_speak']['homeworks'] for value in member_config['teacher']['read_speak']['homeworks'][key].values() if value % 1 == 0]) * target_score / teacher_rs_ex, 2)}")

    user_config = open_data(f"users/{user}.yaml")
    rs = gr.Radio.update(choices=list(user_config['teacher']['read_speak']['homeworks'].keys()))

    return expected_coins, current_rs, rs_hw_df, new_rs_lang, rs

def rs_change(rs):
    global user_config
    user_config = open_data(f"users/{user}.yaml")

    rs_hw_choices = list(user_config['teacher']['read_speak']['homeworks'][rs].keys())
    return gr.Dropdown.update(choices=rs_hw_choices, value=rs_hw_choices[0])

def rs_hw_change(rs, rs_hw):
    user_config = open_data(f"users/{user}.yaml")
    t2v = user_config['teacher']['read_speak']['settings'][rs]['t2v']
    target_score = user_config['teacher']['read_speak']['target_score']
    voice_speed = user_config['teacher']['read_speak']['speed']
    voice = user_config['teacher']['read_speak']['settings'][rs]['voice']
    language = user_config['teacher']['read_speak']['settings'][rs]['language']
    homework = user_config['teacher']['read_speak']['homeworks'][rs]

    if user_config['teacher']['read_speak']['homeworks'][rs][rs_hw] >= target_score:
        audio_mic_return = gr.Audio.update(visible=False, value=None)
        output_text_return = 'Finished! 🎉🎉🎉'
    else:
        audio_mic_return = gr.Audio.update(visible=True, value=None)
        output_text_return = ''

    text2voice(t2v, user, rs_hw, dic['languages'][language][t2v]['code'], voice, voice_speed) # text2voice(t2v, user, text, lang, speed)
    return gr.Audio.update(visible=True, value=f'tmp/{user}/t2v.mp3'), audio_mic_return, output_text_return, gr.Label.update(value=gen_progress(homework, target_score))

def audio_mic_change(audio_mic):
    if audio_mic == None:
        send_button = gr.Button.update(visible=False)
    else:
        send_button = gr.Button.update(visible=True)
    return send_button

def button_send_click(audio_mic, rs, rs_hw):
    global user_config

    user_config = open_data(f"users/{user}.yaml")
    v2t = user_config['teacher']['read_speak']['v2t']
    difficulty = user_config['teacher']['read_speak']['difficulty']
    v2t_model = user_config['teacher']['read_speak']['v2t']
    target_score = user_config['teacher']['read_speak']['target_score']

    text = voice2text(v2t, audio_mic, v2t_model)

    score = (SequenceMatcher(None, clean_text(text), clean_text(rs_hw)).ratio()) ** difficulty
    score = (score * 13) -3
    if score > 6.6:
        emoji = "😁"
    elif score > 3.3:
        emoji = "😐"
    elif score > 0:
        emoji = "😥"
    else:
        emoji = "❗"

    total_score = score + user_config['teacher']['read_speak']['homeworks'][rs][rs_hw]
    if total_score >= target_score:
        result = f"Score: {round(score, 2)} " + emoji + "\nFinished! 🎉🎉🎉"
        audio_mic_return = gr.Audio.update(visible=False, value=None)
    else:
        result = f"Score: {round(score, 2)} " + emoji + "\n\n" + text
        audio_mic_return = gr.Audio.update(visible=True, value=None)

    user_config['teacher']['read_speak']['homeworks'][rs][rs_hw] = total_score
    if user_config['teacher']['read_speak']['settings'][rs]['by'] != user:
        user_config['teacher']['balance'] = user_config['teacher']['balance'] + score / user_config['teacher']['read_speak']['rate']
    balance_text_return = f"{lang['Your balance'][l]}: $ {round(user_config['teacher']['balance'], 2)}"

    homework = user_config['teacher']['read_speak']['homeworks'][rs]

    update_data(f"users/{user}.yaml", user_config)
    return result, gr.Label.update(value=gen_progress(homework, target_score)), audio_mic_return, balance_text_return, gr.Button.update(visible=False)

# -----

user = '100000'
user_config = open_data(f"users/{user}.yaml")
member_config = open_data(f"users/{user}.yaml")
l = user_config['language']
lang = open_data('lang.yaml')
dic = open_data('dic.yaml')

with gr.Blocks(title='IndieAI') as app:
    with gr.Row():
        for i in range(4):
            gr.Markdown(value='')
        warning_msg = gr.Warning('')
        reload_button = gr.Button(value=lang['Reload'][l])
        cancel_button = gr.Button(value=lang['Cancel'][l])

    with gr.Tab('🏠'):
        with gr.Row():
            with gr.Column(scale=4):
                user_welcome = gr.Markdown(value=f"# {lang['Welcome'][l]} {user_config['name']}!")
                user_id = gr.Markdown(value=f"{lang['Your ID'][l]}: {user}", visible=False)
            with gr.Column(scale=1):
                logout_button = gr.Button(value=lang['Logout'][l], visible=False)
                user_lang = gr.Dropdown(show_label=False, choices=dic['web_ui'], value=l, container=False, visible=False)

        with gr.Column():
            login_user = gr.Textbox(label=lang['Your ID'][l], type='text')
            login_pass = gr.Textbox(label=lang['Password'][l], type='password')
            login_button = gr.Button(value=lang['Login'][l])

        with gr.Accordion(f"{lang['Account settings'][l]}", open=False, visible=False) as account_acc:
            with gr.Row():
                user_name = gr.Textbox(label=lang['Name'][l], value=user_config['name'], type='text')
                user_pass = gr.Textbox(label=lang['Password'][l], type='password')
                user_pass2 = gr.Textbox(label=lang['Repeat password'][l], type='password')
            with gr.Row():
                save_us_button = gr.Button(lang['Save'][l])
                gr.Markdown(value='', scale=4)

            user_credentials = gr.Markdown(value=f"### {lang['Credentials'][l]}")
            with gr.Row():
                hf_token = gr.Textbox(label='Hugging face token', type='password')
                openai_token = gr.Textbox(label='OpenAI token', type='password')
                elevenlabs_token = gr.Textbox(label='ElevenLabs token', type='password')
                azure_region = gr.Textbox(label='Azure region', type='text')
                azure_token = gr.Textbox(label='Azure token', type='password')
            with gr.Row():
                save_cred_button = gr.Button(lang['Save'][l])
                gr.Markdown(value='', scale=4)

            user_settings = gr.Markdown(value=f"### {lang['Members'][l]}")
            with gr.Row():
                member_add_id = gr.Textbox(show_label=False, container=False, type='text')
                add_button = gr.Button(lang['Add'][l])
                gr.Markdown(value='', scale=4)
            with gr.Row():
                members = gr.Dropdown(show_label=False, choices=list(user_config['members'].keys()), value=user, container=False)
                del_button = gr.Button(lang['Delete member'][l])
                gr.Markdown(value='', scale=3)

        with gr.Accordion(lang['Teacher settings'][l], open=False, visible=False) as teacher_s_acc:
            with gr.Row():
                teacher_settings_user = gr.Dropdown(show_label=False, value=user, choices=user_config['members'], container=False, scale=1)
                gr.Markdown(value='', scale=4)

            with gr.Accordion(lang['Read and speak'][l], open=False) as teacher_rs_acc:
                with gr.Row():
                    with gr.Column(scale=1):
                        v2t_model = gr.Dropdown(label=lang['Voice to text model'][l], value=member_config['teacher']['read_speak']['v2t'], choices=dic['v2t'])
                        voice_speed = gr.Slider(label=lang['Voice speed'][l], value=member_config['teacher']['read_speak']['speed'], minimum=0.5, maximum=1.0)
                        teacher_rs_ex = gr.Number(label=lang['Exchange rate'][l], value=member_config['teacher']['read_speak']['rate'], minimum=1)
                        target_score = gr.Number(label=lang['Target score'][l], value=member_config['teacher']['read_speak']['target_score'], minimum=1)
                        difficulty = gr.Slider(label=lang["Difficulty"][l], value=member_config['teacher']['read_speak']['difficulty'], minimum=1.0, maximum=5.0)
                        expected_coins = gr.Markdown(f"{lang['Expected coins'][l]}: $ {round(sum([1 for key in member_config['teacher']['read_speak']['homeworks'] for value in member_config['teacher']['read_speak']['homeworks'][key].values() if value % 1 == 0]) * member_config['teacher']['read_speak']['target_score'] / member_config['teacher']['read_speak']['rate'], 2)}")
                    with gr.Column(scale=2):
                        with gr.Row():
                            new_rs = gr.Textbox(show_label=False, container=False, type='text', placeholder=lang['New homework'][l])
                            new_rs_button = gr.Button(lang['New homework'][l])
                        with gr.Row():
                            current_rs = gr.Dropdown(show_label=False, choices=[i for i in list(user_config['teacher']['read_speak']['homeworks'].keys()) if user_config['teacher']['read_speak']['settings'][i]['by'] == user])
                            new_rs_lang = gr.Dropdown(show_label=False, choices=list(dic['languages'].keys()), value='English')
                            t2v_model = gr.Dropdown(show_label=False, value='gTTS', choices=list(dic['languages'][new_rs_lang.value].keys()))
                            new_rs_voice = gr.Dropdown(show_label=False, value='Default', choices='Default')
                        rs_hw_df = gr.Dataframe(headers=['-', lang['Score'][l]], col_count=(2, "fixed"))
                        with gr.Row():
                            save_rs_button = gr.Button(lang['Save'][l])
                            del_rs_button = gr.Button(lang['Delete homework'][l])

    with gr.Tab('🤖 Teacher'):
        balance_text = gr.Markdown(f"{lang['Your balance'][l]}: $ {round(user_config['teacher']['balance'], 2)}")
        with gr.Accordion(lang["Read and speak"][l], open=True) as rs_acc:
            with gr.Row():
                rs = gr.Radio(show_label=False, choices=list(user_config['teacher']['read_speak']['homeworks'].keys()))

            with gr.Row():
                rs_hw = gr.Dropdown(label=lang['Select homework'][l], choices=[])
                audio_example = gr.Audio(label=lang['Listen to this'][l], visible=False)
                audio_mic = gr.Audio(label='🎙️', source="microphone", type="filepath", visible=False)

            with gr.Row():
                with gr.Column():
                    output_text = gr.Textbox(show_label=False, container=False)
                    button_send = gr.Button(lang['Send'][l], visible=False)

                with gr.Column():
                    progress = gr.Label(show_label=False)

    reload_button.click(fn=reload_button_change, outputs=[reload_button, cancel_button,  account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_id, user_lang, login_user, login_pass, login_button, logout_button, user_name, user_pass, user_pass2, save_us_button, user_credentials, save_cred_button, user_settings, add_button, del_button, members, teacher_settings_user, v2t_model, t2v_model, new_rs_voice, voice_speed, teacher_rs_ex, target_score, difficulty, new_rs, new_rs_button, rs_hw_df, save_rs_button, del_rs_button, balance_text, rs_hw, rs, audio_example, button_send])

    # 🏠
    user_lang.change(fn=user_lang_change, inputs=[user_lang], outputs=[reload_button, cancel_button,  account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_id, user_lang, login_user, login_pass, login_button, logout_button, user_name, user_pass, user_pass2, save_us_button, user_credentials, save_cred_button, user_settings, add_button, del_button, members, teacher_settings_user, v2t_model, t2v_model, new_rs_voice, voice_speed, teacher_rs_ex, target_score, difficulty, new_rs, new_rs_button, rs_hw_df, save_rs_button, del_rs_button, balance_text, rs_hw, rs, audio_example, button_send])
    login_button.click(fn=login_button_change, inputs=[login_user, login_pass], outputs=[reload_button, cancel_button,  account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_id, user_lang, login_user, login_pass, login_button, logout_button, user_name, user_pass, user_pass2, save_us_button, user_credentials, save_cred_button, user_settings, add_button, del_button, members, teacher_settings_user, v2t_model, t2v_model, new_rs_voice, voice_speed, teacher_rs_ex, target_score, difficulty, new_rs, new_rs_button, rs_hw_df, save_rs_button, del_rs_button, balance_text, rs_hw, rs, audio_example, button_send])
    logout_button.click(fn=logout_button_change, outputs=[account_acc, teacher_s_acc, teacher_rs_acc, rs_acc, user_welcome, user_lang, user_id, login_user, login_pass, login_button, logout_button, balance_text, rs_hw, rs, audio_example, button_send])

    save_us_button.click(fn=save_us_button_change, inputs=[user_name, user_pass, user_pass2], outputs=[user_welcome])
    save_cred_button.click(fn=save_cred_button_change, inputs=[hf_token, openai_token, elevenlabs_token, azure_region, azure_token])
    add_button.click(fn=add_button_change, inputs=[member_add_id], outputs=[members, teacher_settings_user])
    del_button.click(fn=del_button_change, inputs=[members], outputs=[members, teacher_settings_user])

    teacher_settings_user.change(fn=teacher_settings_user_change, inputs=[teacher_settings_user], outputs=[v2t_model, voice_speed, teacher_rs_ex, target_score, difficulty, expected_coins, new_rs, current_rs, new_rs_lang, t2v_model, new_rs_voice, rs_hw_df])

    v2t_model.change(fn=v2t_model_change, inputs=[teacher_settings_user, v2t_model])
    voice_speed.change(fn=voice_speed_change, inputs=[teacher_settings_user, voice_speed])
    teacher_rs_ex.change(fn=teacher_rs_ex_change, inputs=[teacher_settings_user, teacher_rs_ex, target_score], outputs=[expected_coins])
    target_score.change(fn=target_score_change, inputs=[teacher_settings_user, target_score, teacher_rs_ex], outputs=[expected_coins])
    difficulty.change(fn=difficulty_change, inputs=[teacher_settings_user, difficulty])

    new_rs_button.click(fn=new_rs_button_change, inputs=[teacher_settings_user, new_rs], outputs=[current_rs, rs])
    current_rs.change(fn=current_rs_change, inputs=[teacher_settings_user, current_rs], outputs=[new_rs_lang, rs_hw_df])
    new_rs_lang.change(fn=new_rs_lang_change, inputs=[new_rs_lang], outputs=[t2v_model, new_rs_voice])
    t2v_model.change(fn=t2v_model_change, inputs=[new_rs_lang, t2v_model], outputs=[new_rs_voice])
    save_rs_button.click(fn=save_rs_button_change, inputs=[teacher_settings_user, current_rs, new_rs_lang, t2v_model, rs_hw_df, new_rs_voice, target_score, teacher_rs_ex], outputs=[expected_coins, rs])
    del_rs_button.click(fn=del_rs_button_change, inputs=[teacher_settings_user, current_rs, target_score, teacher_rs_ex], outputs=[expected_coins, current_rs, rs_hw_df, new_rs_lang, rs])

    # 🤖 Teacher 
    rs.change(fn=rs_change, inputs=[rs], outputs=[rs_hw])
    rs_hw.change(fn=rs_hw_change, inputs=[rs, rs_hw], outputs=[audio_example, audio_mic, output_text, progress])
    audio_mic.change(fn=audio_mic_change, inputs=[audio_mic], outputs=[button_send])
    rs_event = button_send.click(fn=button_send_click, inputs=[audio_mic, rs, rs_hw], outputs=[output_text, progress, audio_mic, balance_text, button_send])

    cancel_button.click(fn=cancel_button_change, cancels=[rs_event])
    app.queue()
    app.launch(favicon_path='io2.webp', show_api=False, quiet=True)
