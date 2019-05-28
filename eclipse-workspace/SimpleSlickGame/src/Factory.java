import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;

public class Factory extends GameObject {
	public static final String FACTORY_PATH = "assets/buildings/factory.png" ;
	public static final int TRUCK_COST = 150 ;
	private int pastTime;

	private boolean isBusy = false; 
	
	Factory(double x , double y) throws SlickException{
		setX(x);
		setY(y);
		setImage(FACTORY_PATH);
		
	}

	@Override
	public void update(World world, Camera camera) {
		Input input = world.getInput();
		if(this.equals(world.getSelected())) {
			if(input.isKeyPressed(Input.KEY_1) & world.getMetal() > TRUCK_COST & !isBusy){
				isBusy = true;
				world.setMetal(TRUCK_COST);
			}
		}
		
		if(isBusy) {
			createTruck(world);
		}
	}
	
	
	public void createTruck(World world) {
		if(pastTime > UNIT_BUILD_TIME) {
		
		try {
			isBusy = false;
			pastTime = 0 ;
			GameObject newTruck = new Truck(this.getX() + 30, this.getY() + 30);
			world.addlist.add(newTruck);
		} catch (SlickException e) {
			e.printStackTrace();
		}
		
		}
		else {
			pastTime += world.getDelta();
		}
	}

}
