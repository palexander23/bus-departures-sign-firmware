mod api;

use core::time;
use std::thread;

use tabled::{builder::Builder, settings::Style};

use api::{get_departures, BUSWAY_SHIRE_HALL_N};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut prev_table_line_num = 0;

    loop {
        let departures = get_departures(BUSWAY_SHIRE_HALL_N)?;
        let mut table_builder = Builder::default();

        table_builder.set_header(["Service", "Destination", "Departure"]);

        departures.iter().for_each(|dep| {
            table_builder.push_record([&dep.service, &dep.destination, &dep.time]);
        });

        let mut table = table_builder.build();
        let table = table.with(Style::rounded());

        let table_line_num = table.total_height();

        println!("{}", table);

        thread::sleep(time::Duration::from_secs(2));

        for _ in 0..table_line_num {
            print!("{}", ansi_escapes::CursorPrevLine);
        }

        if prev_table_line_num > table_line_num {
            for _ in 0..prev_table_line_num - table_line_num {
                println!("{}", ansi_escapes::EraseLine);
            }
        }

        prev_table_line_num = table_line_num;
    }
}
