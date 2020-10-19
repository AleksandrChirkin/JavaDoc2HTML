import java.io.*;
import java.util.HashMap;

/**
* Класс-обертка над файлом, содержащим все текущие состояния пользователей
* @author AleksandrChirkin
* @version 1.2
*/
public class StatesOfUsers {
    /** Содержит состояния для всех пользователей, когда-либо обращавшихся к боту*/
    private final HashMap<Long, String> states;

    /** Конструктор считывает из базы данных все текущие состояния пользователей в {@link StatesOfUsers#states}*/
    public StatesOfUsers(){
        states = new HashMap<>();
        File file = new File("./src/statesOfUsers.txt");
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            while (line != null) {
                states.put(Long.valueOf(line.substring(0, line.indexOf("—"))),
                        line.substring(line.indexOf("—") + 1));
                line = reader.readLine();
            }
        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }

    /** Проверяет, обращался ли этот пользователь к боту когда-либо прежде
    * @param id - идентификатор пользователя в Telegram
    */
    public boolean containsKey(long id) {
        return states.containsKey(id);
    }

    /** Возвращает текущее состояние данного пользователя
    * @param id - идентификатор пользователя в Telegram
    */
    public String get(long id){
        return states.get(id);
    }

    /** Добавляет пользователя в базу данных
    * @param id - идентификатор пользователя в Telegram
    * @param str - состояние пользователя
    */
    public void put(long id, String str){
        states.put(id, str);
        update();
    }

    /** Обновляет состояние пользователя
    * @param id - идентификатор пользователя в Telegram
    * @param str - новое состояние пользователя
    */
    public void replace(long id, String str){
        states.replace(id, str);
        update();
    }

    /** Закрепляет обновления базы данных на жестком диске*/
    public void update()
    {
        try {
            File file = new File("./src/statesOfUsers.txt");
            BufferedWriter writer = new BufferedWriter(new FileWriter(file, false));
            for (long id : states.keySet())
                writer.write(String.format("%d—%s\n", id, states.get(id)));
            writer.close();
        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }
}