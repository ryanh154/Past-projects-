/*Written by Ryan Hinson*/
class Prize {
	private String name;
	private int prize;
	public Prize() 
	{
		this.setName("Prize");
		this.setPrize(100);
	}
	
	public Prize(String n, int p) 
	{
		this.setName(n);
		this.setPrize(p);
	}
	
	//Setters and Getters
	public void setName(String n) 
	{
		if (n!=null)
			this.name = n;
	}
	public void setPrize(int p) 
	{
		if (p>=0)
			this.prize = p;
	}
	
	public String getName() 
	{
		return this.name;
	}
	
	public int getPrize() 
	{
		return this.prize;
	}
	
	
	public String toString() 
	{
		return "name: "+this.name+"\nprize: "+this.prize;
	}

}
