import org.newdawn.slick.SlickException;

public class MetalMine extends GameObject {

	public static final String METAL_PATH = "assets/resources/metal_mine.png" ;
	private int metalRemaining = 500;
	
	
	public MetalMine(double x, double y) throws SlickException {
		setX(x);
		setY(y);
		setImage(METAL_PATH);
	}


	@Override
	public void update(World world, Camera camera) {
		if(metalRemaining <= 0) {
			world.removelist.add(this);
		}
		
	}
	
	public int getUnobtaniumRemaining() {
		return metalRemaining;
	}


	public void setUnobtaniumRemaining(int amount) {
		this.metalRemaining -= amount;
	}
}

