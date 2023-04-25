mod api;

use tabled::{
    builder::{self, Builder},
    settings::Style,
};

use api::{get_departures, BUSWAY_SHIRE_HALL_N};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let departures = get_departures(BUSWAY_SHIRE_HALL_N)?;
    let mut table_builder = Builder::default();

    table_builder.set_header(["Service", "Destination", "Departure"]);

    departures.iter().for_each(|dep| {
        table_builder.push_record([&dep.service, &dep.destination, &dep.time]);
    });

    println!("{}", table_builder.build().with(Style::rounded()));

    Ok(())
}
