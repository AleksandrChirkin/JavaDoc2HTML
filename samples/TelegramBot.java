import org.telegram.telegrambots.ApiContextInitializer;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.CallbackQuery;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
* Класс, взаимодействующий с Telegram API и передающий запросы боту на обработку
* @author AleksandrChirkin
* @version 1.2
*/
public class TelegramBot extends TelegramLongPollingBot {
    /** Бот, обрабатывающий все запросы пользователей*/
    private static Bot bot;

    /** Точка запуска программы. Инициализирует {@link TelegramBot#bot}
    * @throws TelegramApiException - если соединение с ботом установить не удалось
    */
    public static void main(String[] a) throws TelegramApiException {
        bot = new Bot();
        ApiContextInitializer.init();
        TelegramBotsApi botsApi = new TelegramBotsApi();
        botsApi.registerBot(new TelegramBot());
    }

    @Override
    /** Получает все запросы пользователей и инициирует процесс их обработки
    * @param update - пришедшее сообщение и вся информация о нем
    */
    public void onUpdateReceived(Update update) {
        String txt;
        long id;
        if (update.hasCallbackQuery()){
            CallbackQuery query = update.getCallbackQuery();
            txt = query.getData();
            id = query.getMessage().getChatId();
        } else {
            Message msg = update.getMessage();
            txt = msg.getText().toLowerCase();
            id = msg.getChatId();
        }
        sendMsg(id, txt);
    }

    /** Передает сообщение боту, получает от него ответ и высылает его пользователю
    * @param id - идентификатор пользователя в Telegram
    * @param txt - запрос пользователя
    */
    private void sendMsg(long id, String txt){
        String response = bot.execute(id, txt);
        SendMessage message = new SendMessage();
        message.enableMarkdown(true);
        message.setChatId(id);
        message.setText(response);
        if (response.equals(""))
            message.setText("Кажется, такого товара нет :(");
        if (!txt.equals("/start") && !txt.contains("https://www.citilink.ru/"))
            setButtons(message, txt);
        try{
            execute(message);
        } catch (TelegramApiException e){
            throw new RuntimeException(e);
        }
    }

    /** Прикрепляет к сообщению слой с кнопками
    * @param message - сообщение, к которому будет прикреплен слой с кнопками
    * @param initialRequest - запрос пользователя
    */
    private void setButtons(SendMessage message, String initialRequest){
        HashMap<String, String> categories = bot.relevantCategories(initialRequest);
        if (categories == null || categories.size() == 0) {
            message.setText("Кажется, товаров такой категории у нас нет");
            return;
        } else
            message.setText("Мы нашли Ваш товар в следующих категориях:");
        InlineKeyboardMarkup keyboardMarkup = new InlineKeyboardMarkup();
        message.setReplyMarkup(keyboardMarkup);
        List<List<InlineKeyboardButton>> keyboard = new ArrayList<>();
        for (String category : categories.keySet()) {
            List<InlineKeyboardButton> currentRow = new ArrayList<>();
            keyboard.add(currentRow);
            currentRow.add(new InlineKeyboardButton().setText(category)
                        .setCallbackData(categories.get(category)));
        }
        keyboardMarkup.setKeyboard(keyboard);
    }

    @Override
    /** Используется для получения Telegram API имени бота*/
    public String getBotUsername() {
        return System.getenv("CONSULTANT_BOT_NAME");
    }

    @Override
    /** Используется для получения Telegram API токена бота*/
    public String getBotToken() {
        return System.getenv("CONSULTANT_BOT_TOKEN");
    }
}
