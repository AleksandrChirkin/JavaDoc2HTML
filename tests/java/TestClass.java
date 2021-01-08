package javadoc2html.tests;

import javadoc2html.tests.TestInterface;


/**
 * Class created for unittest
 * @author UserName
 * @version 1.1
 * @since   1.0
 * @see TestInterface
*/

public class TestClass implements TestInterface
{
    private Map<Integer, String> values;
    boolean value = true;

    /**
    * Class Constructor
    * @param value boolean
    * @exception IOException
    * @throws ParseException
    */
    TestClass(boolean value)
    {
        this.value = value;
    }

    /**
    * @return Map<Integer, String> Key - index, value - string
    */
    Map<Integer, String> getValues()
    {
        return values;
    }

    /**
    * @return String
    * @param index Integer
    * It is super class of {@link TestInterface}
    */
    String getString(Integer index)
    {
        return values.get(index);
    }

    boolean getValue()
    {
        return value;
    }

    /**
    *  Method for adding a new string to Map
    *  @param index
    *  @param string
    */
    void addString(Integer index, String string)
    {
        if(!values.containsKey(index))
        {
            values.put(index, string);
        }
    }
}