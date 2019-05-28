import java.util.ArrayList;

import org.newdawn.slick.Input;
import org.newdawn.slick.SlickException;

public class CommandCentre extends GameObject {
	public static final String COMMAND_CENTRE_PATH = "assets/buildings/command_centre.png" ;
	public static final int SCOUT_COST = 5;
	public static final int BUILDER_COST = 10; 
	public static final int ENGINEER_COST = 20; 
	private boolean isTrainingScout = false;
	private boolean isTrainingBuilder = false;
	private boolean isTrainingEngineer = false;
	private boolean isBusy = false;
	private int pastTime ; 
	
	public CommandCentre(double x, double y) throws SlickException {
		setX(x);
		setY(y);
		setImage(COMMAND_CENTRE_PATH);
	}


	@Override
	public void update(World world, Camera camera) {
		Input input = world.getInput();
		
		if(this.equals(world.getSelected())) {
			if (input.isKeyPressed(Input.KEY_1) & world.getMetal() > SCOUT_COST & !isBusy){
				isBusy = true;
				isTrainingScout = true;		
				world.setMetal(SCOUT_COST);
			}
			
			if (input.isKeyPressed(Input.KEY_2) & world.getMetal() > BUILDER_COST & !isBusy ){
				isBusy = true;
				isTrainingBuilder = true;
				world.setMetal(BUILDER_COST);	
				}
			if (input.isKeyPressed(Input.KEY_3) & world.getMetal() > ENGINEER_COST & !isBusy){
				    isBusy = true;
					isTrainingEngineer = true;	
					world.setMetal(ENGINEER_COST);
			}		
		}	
		
		if(isTrainingScout) {
			createScout(world);
		}
		if(isTrainingBuilder) {
			createBuilder(world);
		}
		if(isTrainingEngineer) {
			createEngineer(world);
		}
			
	}
	
	
	public void createScout(World world) {
		
		if(pastTime > UNIT_BUILD_TIME) {
		try {
			isTrainingScout = false;
			isBusy = false;
			GameObject newScout = new Scout(this.getX()+30 , this.getY()+ 30);
			pastTime = 0;
			world.addlist.add(newScout);
			
		} catch (SlickException e) {
			e.printStackTrace();
			}			
		}
		else {
			pastTime += world.getDelta();
		}
	}
	
	
	public void createBuilder(World world) {
		if(pastTime > UNIT_BUILD_TIME) {
		
		try {
			isTrainingBuilder = false;
			isBusy = false;
			pastTime = 0 ;
			GameObject newBuilder = new Builder(this.getX() + 30, this.getY() + 30);
			world.addlist.add(newBuilder);
		} catch (SlickException e) {
			e.printStackTrace();
		}
		
		}
		else {
			pastTime += world.getDelta();
		}
	}
	
	
	public void createEngineer(World world){
		if(pastTime > UNIT_BUILD_TIME) {
		try {
			
			isTrainingEngineer = false;
			isBusy = false;
			pastTime = 0;
			GameObject newEngineer = new Engineer(this.getX() + 30 , this.getY() + 30 );
			world.addlist.add(newEngineer);
		} catch (SlickException e) {
			e.printStackTrace();
		}
		
	}
	else {
		pastTime += world.getDelta();
	}
		
		
	}
	
	
	}
	

