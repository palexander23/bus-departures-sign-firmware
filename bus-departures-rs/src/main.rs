mod api;

use api::{get_departures, BUSWAY_SHIRE_HALL_N};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Hello, world!");

    let departures = get_departures(BUSWAY_SHIRE_HALL_N)?;

    departures
        .iter()
        .for_each(|departure| println!("{:?}", departure));

    Ok(())
}
