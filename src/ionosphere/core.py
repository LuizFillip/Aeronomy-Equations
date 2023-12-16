import ionosphere as io
import atmosphere as atm


def conductivity_parameters(df):
    
    """
    Compute collision frequencies and 
    and ionospheric conductivities
    """


    nu = io.collision_frequencies()

    df["nui"] = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )

    df["nue"] = nu.electrons_neutrals2(
        df["O"], 
        df["O2"], 
        df["N2"],
        df["He"], 
        df["H"],
        df["Te"]
        )

    df['perd'] = io.conductivity(
        B = df['Bf'] 
        ).pedersen(
        df["Ne"], 
        df["nui"], 
        df["nue"]
        )

    df['R'] = atm.recombination2(
        df["O2"], 
        df["N2"]
        )


    return df
