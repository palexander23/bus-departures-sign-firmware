use lazy_static::lazy_static;
use regex::Regex;
use reqwest::blocking::Client;

const URL_TEMPLATE: &str =
    "http://www.cambridgeshirebus.info/Popup_Content/WebDisplay/WebDisplay.aspx?stopRef=";

// Bus Stop IDs
pub const BUSWAY_SHIRE_HALL_N: &str = "0500CCITY497";

// Regexes
lazy_static! {
    static ref DEP_TIME_REGEX: Regex = Regex::new(r#"meItem"[^<]+>([^<]+)<"#).unwrap();
    static ref DEP_SERVICE_REGEX: Regex = Regex::new(r#"ceItem"[^<]+>([^<]+)<"#).unwrap();
    static ref DEP_DEST_REGEX: Regex = Regex::new(r#"ionItem" [^>]+><[^>]+>([^<]+)<"#).unwrap();
}

#[derive(Debug)]
pub struct DepartureTimeInfo {
    time: String,
    service: String,
    destination: String,
}

fn get_departure_html(stop_id: &str) -> Result<String, Box<dyn std::error::Error>> {
    let url = format!("{}{}", URL_TEMPLATE, stop_id);
    let client = Client::new();
    let response = client.get(&url).send()?;
    if response.status().is_success() {
        let content = response.text()?;
        Ok(content)
    } else {
        Err(format!("URL returned an invalid response: {:?}", response).into())
    }
}

fn get_departure_objs(departures_html: &str) -> Vec<DepartureTimeInfo> {
    // Split the HTML into lines
    let html_lines = departures_html.split("\r\n");

    // Get the lines containing departure times
    let lines: Vec<_> = html_lines
        .filter(|line| line.contains("gridDestinationItem"))
        .collect();

    let times: Vec<String> = lines
        .iter()
        .filter_map(|line| DEP_TIME_REGEX.captures(line).map(|c| c[1].to_string()))
        .collect();
    let services: Vec<String> = lines
        .iter()
        .filter_map(|line| DEP_SERVICE_REGEX.captures(line).map(|c| c[1].to_string()))
        .collect();
    let destinations: Vec<String> = lines
        .iter()
        .filter_map(|line| DEP_DEST_REGEX.captures(line).map(|c| c[1].to_string()))
        .collect();

    times
        .into_iter()
        .zip(services)
        .zip(destinations)
        .map(|((time, service), destination)| DepartureTimeInfo {
            time,
            service,
            destination,
        })
        .collect()
}

pub fn get_departures(stop_id: &str) -> Result<Vec<DepartureTimeInfo>, Box<dyn std::error::Error>> {
    let departures_html = get_departure_html(stop_id)?;
    let departure_objs = get_departure_objs(&departures_html);
    Ok(departure_objs)
}
