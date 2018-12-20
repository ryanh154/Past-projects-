/*Written By Ryan Hinson*/
import java.util.*;
import java.util.Random;
import java.io.*;
public class Showcase {
	
	public static String DELIM = "\t";
	public static int LIST_LENGTH = 5;
	public static String MY_FILE = "src/prizeList.txt";
	
	Prize[] showList = new Prize[LIST_LENGTH];
	
	public Showcase() 
	{
		this.setShowList();
	}
	
	
	public void setShowList() 
	{
		Random rand = new Random();
		//create arrays
		Prize[] prizeList = readFromFile(MY_FILE);
		

		for (int i=0;i<LIST_LENGTH;i++) 
		{
			int r = rand.nextInt(prizeList.length-1);
			
			this.showList[i] = prizeList[r];
		}
	}
	
	
	
	public String toString() 
	{
		String List = "";
		
		for (int i=0;i<LIST_LENGTH;i++) 
		{
			List+= this.showList[i].getName()+"\n";
		}
		return List;
	}
	
	//get total of all the prizes
	public int getTotal() 
	{
		int Total =0;
		
		for (int i=0;i<LIST_LENGTH;i++) 
		{
			Total+=this.showList[i].getPrize();
		}
		return Total;
	}
	
	
	public static Prize[] readFromFile(String fileName) 
	{
		if (fileName==null)
			return null;
		
		try 
		{
			
			Scanner fileScanner = new Scanner(new File(fileName));
			
			int prizeCount = 0;
			
			while(fileScanner.hasNextLine()) 
			{
				prizeCount++;
				fileScanner.nextLine();
			}
			
			
			fileScanner = new Scanner(new File(fileName));
			String fileLine;
			String splitString[];
			Prize[] retPrize = new Prize[prizeCount];
			
			
			int prizeFileCount = 0;
			while(fileScanner.hasNextLine()) 
			{
				fileLine = fileScanner.nextLine();
				splitString = fileLine.split(DELIM);
				if (splitString.length == 2) 
				{
					String name = splitString[0];
					String prize = splitString[1];
					retPrize[prizeFileCount] = new Prize(name, Integer.parseInt(prize));
					prizeFileCount++;
				}
			}
			fileScanner.close();
			return retPrize;
			
		}
		catch(Exception e) 
		{
			System.out.println(e);
		}
		
		return null;
	}
	

}
