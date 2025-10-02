def beta_calc(wavelength_source, wavelength_observed):
    beta = ((wavelength_observed**2 - wavelength_source**2)/
            (wavelength_observed**2 + wavelength_source**2))

    return beta


c = 299792458 #m/s
b = beta_calc(650,645)
print("v/c =",b)
print("v = ",b*c,"m/s = ",(b*c)/1000,"km/s")