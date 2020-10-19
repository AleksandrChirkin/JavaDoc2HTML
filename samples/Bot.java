import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONObject;

/**
* Класс бота, обрабатывающий вызов, полученный TelegramBot
* @author AleksandrChirkin
* @version 1.2
*/
public class Bot {
    /** Содержит последнюю загруженную страницу*/
    private String response;
    /** Категории товаров на сайте citilink.ru*/
    private final HashMap<String, String> categories;
    /** Содержит все текущие состояния пользователей*/
    private final StatesOfUsers states;

    /** Конструктор загружает в {@link Bot#response} главную страницу citilink,
     * извлекает из нее в {@link Bot#categories} категории
     * и восстанавливает из физической памяти в {@link Bot#states} состояния пользователей на момент выключения бота
     */
    public Bot(){
        getResponse("");
        states = new StatesOfUsers();
        categories = getCategories();
    }

    /** Принимает запрос пользователя и передает его на обработку
     * @param id - идентификатор пользователя в Telegram
     * @param request - запрос пользователя
     */
    public String execute(long id, String request) {
        try {
            String hostLink = "https://www.citilink.ru/";
            if (request.equals("/start"))
                return "Бот-консультант. Ищет нужный Вам товар в ситилинке\n" +
                        "Введите нужный Вам товар:";
            if (request.contains(hostLink))
            {
                getResponse(request.substring(hostLink.length()));
                return findItems(id);
            }
            if (!states.containsKey(id))
                states.put(id, "");
            states.replace(id, request);
            return "";
        } catch (Exception e){
            return ("Произошла ошибка. Попробуйте еще раз");
        }
    }

    /** Находит по запросу пользователя подходящие категории
     * @param request - запрос пользователя
     */
    public HashMap<String, String> relevantCategories(String request){
        if (categories == null)
            return null;
        HashMap<String, String> result = new HashMap<>();
        String[] words = request.split(" ");
        for (String category: categories.keySet())
            for (String item: category.split(" "))
                for (String word: words)
                    if (item.toLowerCase().contains(word.toLowerCase()))
                        result.put(category, categories.get(category));
        return result;
    }

    /**Находит на главной странице citilink.ru категории*/
    private HashMap<String, String> getCategories(){
        if (response == null)
            return null;
        String categoriesString = response.substring(response.indexOf("<menu"));
        String[] allLines = categoriesString.substring(0, categoriesString.indexOf("</menu")).split("\n");
        HashMap<String, String> categories = new HashMap<>();
        String currentReference = "";
        for (String line: allLines){
            if (line.contains(" href"))
                currentReference = line.substring(line.indexOf("\"")+1, line.length()-1);
            else if (!currentReference.equals("")){
                if (line.contains(">"))
                    continue;
                categories.put(line.strip(), currentReference);
                currentReference = "";
            }
        }
        return categories;
    }

    /** Перевод найденную страницу в удобный для пользователя формат
    * @param id - идентификатор пользователя в Telegram
    */
    private String findItems(long id) {
        String[] allLines = response.split("\n");
        ArrayList<String> lines = new ArrayList<>();
        String trigger = "data-params=\"";
        for (String line: allLines)
            if (line.contains(trigger))
                lines.add(line.substring(line.indexOf(trigger) + trigger.length()));
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < lines.size(); i+=2) {
            String processedLine = processLine(lines.get(i));
            String[] words = states.get(id).split(" ");
            for (String word: words)
                if (processedLine != null &&
                        processedLine.toLowerCase().contains(word.toLowerCase())) {
                    result.append(processedLine);
                    result.append("\n");
                }
        }
        return result.toString();
    }

    /** Обрабатывает строку, содержащую полную информацию о товаре, и возвращает только самую нужную
    * @param line - строка, взятая из HTML-страницы
    */
    private String processLine(String line) {
        line = line.replace("&quot;", "\"");
        JSONObject json = new JSONObject(line);
        return (json.has("price"))
                ? String.format("*_%s_*\n*Бренд:*%s\n*Цена:*%d\n", json.get("shortName"), json.get("brandName"),
                Integer.valueOf(json.get("price").toString()))
                : null;
    }

    /** Выстраивает соединение с citilink.ru и получает по нему ответ на запрос
    * @param txt - запрос
    */
    private void getResponse(String txt){
        HttpURLConnection connection = null;
        try {
            URL url = new URL(String.format("https://www.citilink.ru/%s", txt));
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type",
                    "application/x-www-form-urlencoded");
            connection.setRequestProperty("Content-Language", "en-US");
            connection.setUseCaches(false);
            connection.setDoOutput(true);
            DataOutputStream wr = new DataOutputStream (connection.getOutputStream());
            wr.close();
            BufferedReader rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            StringBuilder result = new StringBuilder();
            while ((line = rd.readLine()) != null) {
                result.append(line);
                result.append('\n');
            }
            rd.close();
            response = result.toString();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
