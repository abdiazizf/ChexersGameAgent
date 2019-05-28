import org.newdawn.slick.SlickException;

public class UnobtainiumMine extends GameObject {
	public static final String UNOBTANIUM_PATH = "assets/resources/unobtainium_mine.png" ;
	private int unobtaniumRemaining = 50;

	UnobtainiumMine(double x, double y) throws SlickException{
		setX(x);
		setY(y);
		setImage(UNOBTANIUM_PATH);
	}


	@Override
	public void update(World world, Camera camera) {
		if(unobtaniumRemaining <= 0) {
			world.removelist.add(this);
		}
		
	}


	public int getUnobtaniumRemaining() {
		return unobtaniumRemaining;
	}


	public void setUnobtaniumRemaining(int amount) {
		this.unobtaniumRemaining -= amount;
	}
}
