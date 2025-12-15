
import sys
import os
import json
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def render_stl(stl_path, output_png_path):
    try:
        import pyvista as pv
        pv.OFF_SCREEN = True
        
        # Create plotter
        plotter = pv.Plotter(off_screen=True, window_size=[800, 600])
        
        # Load mesh
        mesh = pv.read(stl_path)
        
        # Add mesh to scene
        plotter.add_mesh(mesh, color='gold', show_edges=True, edge_color='black', pbr=True, metallic=0.3)
        plotter.add_axes()
        plotter.show_grid()
        plotter.set_background('#1A1A1A')
        plotter.camera_position = 'iso'
        
        # Render
        plotter.screenshot(output_png_path)
        plotter.close()
        return True
    except Exception as e:
        logging.error(f"PyVista render failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print(json.dumps({'status': 'error', 'message': 'Usage: renderer.py input.stl output.png'}))
            sys.exit(1)

        stl_path = sys.argv[1]
        png_path = sys.argv[2]
        
        if not os.path.exists(stl_path):
            print(json.dumps({'status': 'error', 'message': f'STL file not found: {stl_path}'}))
            sys.exit(1)
            
        success = render_stl(stl_path, png_path)
        
        if success:
            print(json.dumps({'status': 'success', 'png_path': png_path}))
        else:
            print(json.dumps({'status': 'error', 'message': 'Rendering failed'}))
            
    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}))
        sys.exit(1)
