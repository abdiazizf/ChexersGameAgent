import org.newdawn.slick.SlickException;

public class Pylon extends GameObject {
	public static final String PYLON_PATH = "assets/buildings/pylon.png" ;
	public static final String PYLON_ACTIVE_PATH = "assets/buildings/pylon_active.png" ;
	
	Pylon(double x, double y) throws SlickException{
		setX(x);
		setY(y);
		setImage(PYLON_PATH);
	}

	@Override
	public void update(World world, Camera camera) {
		// TODO Auto-generated method stub
		
	}

}
