import brukeropusreader
import numpy as np
import sys

filename = sys.argv[1]
opus_data = brukeropusreader.read_file(filename)

with open(filename+'.hdr', 'w') as hdr_file:
    with open(filename+'.dat', 'w') as dat_file:
        
        ### File Parameters ###
        day = opus_data["IgSm Data Parameter"]['DAT']
        wstart = opus_data["IgSm Data Parameter"]['FXV']
        wstop = opus_data["IgSm Data Parameter"]['LXV']
        npo = opus_data["IgSm Data Parameter"]['NPT']
        delw = 1
        resolutn = opus_data["Acquisition"]['RES']
        ### Scan Parameters ###
        alias = 1
        fdr = 2 * (opus_data["Instrument"]['SSM'] / opus_data["Instrument"]['SSP'])
        refwavno = opus_data["Instrument"]['LWN']
        fclock = 1
        sampfreq = 1
        ### Transform Parameters ###
        nint = npo
        ntrans = 2097152
        freespec = opus_data["Instrument"]['HFL'] 
        
        ### Write interferogam header ###
        hdr_file.writelines(
            f'/         FILE PARAMETERS\n'
            f'id      = NSO type 6 FTS data file     \n'                                       
            f'day     = {day}        / Acquisition date \n'
            f'wstart  = {wstart}              / First wavenumber / point in file\n'
            f'wstop   = {wstop}         / Last wavenumber / point in file\n'
            f'npo     = {npo}                / Number of points in file\n'
            f'data_is = Real                 / Data ARE Real or Complex\n'
            f'delw    = {delw}                 / Dispersion (1/cm / point)\n'
            f'resolutn= {resolutn}               / Spectral resolution (1/cm)\n'
            f'fboffs  = 0                     / File byte offset\n'
            f'bocode  = 0                     / Data byte order: 0=little endian; 1=big endian\n'
            f'xaxis_is= Index                 / Wavenumber, Wavelength, Index, Other\n'
            f'/         SCAN PARAMETERS\n'
            f'alias   = {alias}               / Alias\n'
            f'fdr     = {fdr}                 / Samples per laser fringe (fringe div. ratio)\n'
            f'drivevel= 2000.0                / Carriage velocity in fringes / sec\n'
            f'refwavno= {refwavno}            / Laser wavenumber (1/cm)\n'
            f'fclock  = {fclock}              / Sampling clock frequency (Hz)\n'
            f'sampfreq= {sampfreq}            / Sampling frequency (Hz)\n'
            f'/         TRANSFORM PARAMETERS\n'
            f'nint    = {nint}                / Number of pts in interferogram\n'
            f'ntrans  = {ntrans}               / Transform size (2**N)\n'
            f'freespec= {freespec}          / Free spectral range (1/cm)\n'
            f'END'
            )
        
        ### Write interferogram dat file ###
        dat_data = np.array(opus_data["IgSm"], dtype=np.float32)  # convert interferogram datapoints to 32-bit floats
        dat_data.tofile(dat_file)  # write interferogram data to binary file
        
with open(filename+'_r.hdr', 'w') as hdr_spe:
    with open(filename+'_r.dat', 'w') as spe_file:

        ### Write spectrum header ###
        hdr_spe.writelines(
            f'/         FILE PARAMETERS\n'
            f'id      = NSO type 6 FTS data file     \n'                                       
            f'day     = {day}        / Acquisition date \n'
            f'wstart  = {wstart}              / First wavenumber / point in file\n'
            f'wstop   = {wstop}         / Last wavenumber / point in file\n'
            f'npo     = {npo}                / Number of points in file\n'
            f'data_is = Real                 / Data ARE Real or Complex\n'
            f'delw    = {delw}                 / Dispersion (1/cm / point)\n'
            f'resolutn= {resolutn}               / Spectral resolution (1/cm)\n'
            f'fboffs  = 0                     / File byte offset\n'
            f'bocode  = 0                     / Data byte order: 0=little endian; 1=big endian\n'
            f'xaxis_is= Index                 / Wavenumber, Wavelength, Index, Other\n'
            f'/         SCAN PARAMETERS\n'
            f'alias   = {alias}               / Alias\n'
            f'fdr     = {fdr}                 / Samples per laser fringe (fringe div. ratio)\n'
            f'drivevel= 2000.0                / Carriage velocity in fringes / sec\n'
            f'refwavno= {refwavno}            / Laser wavenumber (1/cm)\n'
            f'fclock  = {fclock}              / Sampling clock frequency (Hz)\n'
            f'sampfreq= {sampfreq}            / Sampling frequency (Hz)\n'
            f'/         TRANSFORM PARAMETERS\n'
            f'nint    = {nint}                / Number of pts in interferogram\n'
            f'ntrans  = {ntrans}               / Transform size (2**N)\n'
            f'freespec= {freespec}          / Free spectral range (1/cm)\n'
            f'END'
            )
        
        ### Write spectrum .dat file ###
        spe_data = np.array(opus_data["ScSm"], dtype=np.float32)  # convert spectrum datapoints to 32-bit floats
        spe_data.tofile(spe_file)  # write spectrum data to binary file