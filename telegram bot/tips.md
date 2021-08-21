### Функция с запуском команды в терминале линукса

    from telegram.ext import ConversationHandler
    import subprocess 
    def ipaddr(bot, update):
        command = "ping -c 4 " + str(update.message.text)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)
        update.message.reply_text(output)
    
        return ConversationHandler.END