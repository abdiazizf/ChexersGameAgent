import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;

public class Builder extends GameObject {
	public static final String BUILDER_PATH = "assets/units/builder.png" ;
	public static final double BUILDER_SPEED = 0.1;
	public static final int FACTORY_COST = 100;
	public static final int FACTORY_BUILD_TIME = 10000;
	private int pastTime; 
	private boolean isBuildingFactory = false;
	public Builder(double x, double y) throws SlickException {
		setX(x);
		setY(y);
		setTargetY(y);
		setTargetX(x);
		setImage(BUILDER_PATH);
		// TODO Auto-generated constructor stub
	}
	
	public void update(World world, Camera camera) {
		Input input = world.getInput();
		// If the mouse button is being clicked, set the target to the cursor location
		if(world.getSelected() == this) {
			if (input.isMousePressed(Input.MOUSE_RIGHT_BUTTON)) {
				setTargetX(camera.screenXToGlobalX(input.getMouseX()));
				setTargetY(camera.screenYToGlobalY(input.getMouseY()));
			}
		
		if(input.isKeyPressed(Input.KEY_1) & world.getMetal() > FACTORY_COST & !isBuildingFactory)
		{
			if(world.isBuildable(getX() + 10 , getX()+ 10));
			isBuildingFactory = true;
			world.setMetal(FACTORY_COST);
			
		}
		}
		// If we're close to our target, reset to our current position
		if (World.distance(getX(), getY(), getTargetX(), getTargetY()) <= BUILDER_SPEED) {
			resetTarget();
		} else {
			// Calculate the appropriate x and y distances
			double theta = Math.atan2(getTargetY() - getY(), getTargetX() - getX());
			double dx = (double)Math.cos(theta) * world.getDelta() * BUILDER_SPEED;
			double dy = (double)Math.sin(theta) * world.getDelta() * BUILDER_SPEED;
			// Check the tile is free before moving; otherwise, we stop moving
			if (world.isPositionFree(getX() + dx, getY() + dy)) {
				setX(getX() + dx);
				setY(getY() + dy);
			} else {
				resetTarget();
			}
		}
		
		
		if(isBuildingFactory) {
			buildFactory(world);
		}
	}
	
	
	public void buildFactory(World world) {
		if(pastTime > FACTORY_BUILD_TIME) {
			try {
				isBuildingFactory = false;
				pastTime= 0 ;
				GameObject newFactory = new Factory(this.getX()+10, this.getY() + 10);
				world.addlist.add(newFactory);
			} catch (SlickException e) {
				e.printStackTrace();
			}
		}
		else {
			pastTime += world.getDelta();
		}
		
	}
	
	
	
}
