/*Written By Ryan Hinson*/
import java.util.*;
public class ShowcaseGame {
	
	public static void main(String[] args) 
	{
		Scanner keyboard = new Scanner(System.in);
		
		System.out.println("WELCOME TO THE SHOWCASE SHOWDOWN!");
		String input = "";
		
		while(!input.equals("no"))
		{
			System.out.println("YOUR PRIZES ARE:");
			
			Showcase list = new Showcase();
			System.out.println(list.toString());
			
			System.out.println("\n"+"YOU MUST GUESS THE TOTAL OF THESE PRIZES WITHOUT GOING OVER!");
			
			
			
			System.out.print("YOUR GUESS:");
			int guess = keyboard.nextInt();
			keyboard.nextLine();
			
			//check the guess to the actual number
			if (guess<=list.getTotal() ) 
			{
				System.out.println("YOUR GUESS WAS "+guess+". THE ACTUAL WAS "+list.getTotal()+". YOU WIN");
			}
			else 
			{
				System.out.println("YOUR GUESS WAS "+guess+". THE ACTUAL WAS "+list.getTotal()+". YOU LOSE.");
			}
			
			System.out.println("Would you like to play again? enter no to Quit");
			input = keyboard.nextLine().toLowerCase();
		}
		keyboard.close();
		System.out.println("GOODBYE");
			
	}

}
