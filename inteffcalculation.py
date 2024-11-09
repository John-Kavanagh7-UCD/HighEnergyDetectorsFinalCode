import numpy as np
import abseffcalculation as abseff


# function to calculate the geometric factor G
# G relates the detector location to the source
# it is how much of the radiation sphere is covered by the detector.
def geometryfactor_squaredetector():

    # take user input to set the location and size of the detector
    L = float(input("Input the width of the aperture of the detector in cm:", ))
    H = float(input("Input the height of the aperture of the detector in cm: "))
    d = float(input("Input the distance from the source to the aperture of the detector in cm:", ))

    L_err = float(input("Input the measurement error for width of the aperture of the detector in cm:", ))
    H_err = float(input("Input the measurement error for height of the aperture of the detector in cm:", ))
    d_err = float(input("Input the measurement error for distance from the source to the aperture of the detector in cm:", ))
    
    # calculate the length of the radiation sphere covered by the detector in each direction
    theta_x = 2 * (np.arctan(L / (2 * d)))
    theta_y = 2 * (np.arctan(H / (2 * d)))

    # calculate the error in theta_x and theta_y
    # calculate the partial derivatives for theta_x and theta_y for both L and d 
    # plug the partial derivatives into the propogation error eqn for general functions
    # for time, partial derivatives computed using computational intelligence 'WolframAlpha'
    # https://www.wolframalpha.com/
    pd_x_wrt_L = (2 * d) / (L**2 + 4 * d**2)
    pd_x_wrt_d = (2 * L) / (L**2 + 4 * d**2)
    pd_y_wrt_H = (2 * d) / (H**2 + 4 * d**2)
    pd_y_wrt_d = (2 * H) / (H**2 + 4 * d**2)

    thetax_error = np.sqrt((pd_x_wrt_L * L_err)**2 + (pd_x_wrt_d * d_err)**2) 
    thetay_error = np.sqrt((pd_y_wrt_H * H_err)**2 + (pd_y_wrt_d * d_err)**2) 
    
    # solid angle subtended by the detector area
    omega = 4 * np.arcsin(np.sin(theta_x / 2) * np.sin(theta_y / 2))

    # calculate the error in omega 
    # calculate the partial derivatives for omega for both theta_x and theta_y
    # plug the partial derivatives into the propogation error eqn for general functions
    # for time, partial derivatives computed using computational intelligence 'WolframAlpha'
    # https://www.wolframalpha.com/
    pd_omega_wrt_x = ((np.cos(theta_x/2) * np.sin(theta_y/2)) / 
        (2 * np.sqrt( 1 - ((np.sin(theta_x/2))**2) * ((np.sin(theta_y/2))**2))))
    pd_omega_wrt_y = ((np.cos(theta_y/2) * np.sin(theta_x/2)) / 
        (2 * np.sqrt( 1 - ((np.sin(theta_x/2))**2) * ((np.sin(theta_y/2))**2))))
    
    omega_error = np.sqrt((pd_omega_wrt_x * thetax_error)**2 + (pd_omega_wrt_y * thetay_error)**2) 
    
    
    # geometric factor is the ratio of solid angle subtended by the detector area to total sphere solid angle 4pi
    G = omega / (4 * np.pi)

    # calculate G error from omega error
    G_error = omega_error / (4 * np.pi)

    return G, G_error

def geometricfactor_circledetector():
    # take user input to set the location and size of the detector
    R = float(input("Input the radius of the aperture of the detector in cm:", ))
    d = float(input("Input the distance from the source to the aperture of the detector in cm:", ))

    R_err = float(input("Input the measurement error for radius of the aperture of the detector in cm:", ))
    d_err = float(input("Input the measurement error for distance from the source to the aperture of the detector in cm:", ))

    # calculate the angle of arc from the centre of the detector to the edge of the detector
    theta = np.arctan(R/d)

    # calculate solid angle subtended by the detector
    omega = 2 * np.pi * (1 - np.cos(theta))

    # geometric factor is the ratio of solid angle subtended by the detector area to total sphere solid angle 4pi
    G = omega / (4 * np.pi)

    # for error propogation
    # partial derivatives of theta
    pd_theta_wrt_R = d / ((d**2) + (R**2))
    pd_theta_wrt_d = R / ((d**2) + (R**2))

    # error in theta by the error propogation eqn
    theta_error = np.sqrt((pd_theta_wrt_R * R_err)**2 + (pd_theta_wrt_d * d_err)**2) 

    # propogate theta_error through the equation to get error in G
    omega_error = 2 * np.pi * (1 - np.cos(theta_error))
    G_error = omega_error / (4 * np.pi)


    return G, G_error

# function to calculate the intrinsic efficiency vs energy
def intrinsic_eff_calculation(calibration_filename, output_file):

    # call the absolute efficiency, energies and geometric factor 
    absolute_efficiency, energy_sorted, abseff_error = abseff.calc_absolute_eff(calibration_filename, output_file)
    
    # request user input for detector shape
    detector_shape = input("input the detector shape (valid inputs: circle, rectangle):",)

    # call the geometric parameter depending on detector shape
    if detector_shape == 'rectangle':    
        G, G_error = geometryfactor_squaredetector()
    elif detector_shape == 'circle':    
        G, G_error = geometricfactor_circledetector()
        
    # calculate intrinsic efficiency
    intrinsic_efficiency =  absolute_efficiency * G
    
    # calcualte error of intrinsic efficiency
    # using product rule for error propogation
    inteff_error = intrinsic_efficiency * ( np.sqrt(((abseff_error/absolute_efficiency)**2) + ((G_error/G)**2)))

    # model a quadratic polynomial to the data and create arrays of values to plot the model
    energy = np.linspace(min(energy_sorted), max(energy_sorted), 100)
    quadratic_fit_coeffs = np.polyfit(np.log(energy_sorted), np.log(intrinsic_efficiency), 2)
    a,b,c = quadratic_fit_coeffs
    efficiency_model = np.exp(a * np.log(energy)**2 + b * np.log(energy) + c)

    return energy_sorted, intrinsic_efficiency, inteff_error, energy, efficiency_model