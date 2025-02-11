import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans

lass_text = "Lassie is a fictional female Rough Collie dog and is featured in a 1938 short story by Eric Knight that was later expanded to a 1940 full-length novel, Lassie Come-Home."
benj_text = "Benji is a fictional canine character created by Joe Camp. He has been the focus of several feature films and other media, beginning with the independently produced 1974 film."
red_text = "Secretariat (March 30, 1970 – October 4, 1989), also known as Big Red, was a champion American thoroughbred racehorse who was the ninth winner of the American Triple Crown, setting and still holding the fastest time record in all three of its constituent races."
full_text = lass_text + benj_text + red_text

nlp = spacy.load("en_core_web_sm")
doc = nlp(full_text)
matcher= Matcher(nlp.vocab)

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.shape_, token.is_alpha, token.is_stop)

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

pattern = [
    {"POS": "PROPN","OP": "*"},
    {"LEMMA": "be"},
    {"LOWER": "a"},
    {"POS": {"IN": ["NOUN", "ADJ"]}, "OP": "*"},
    {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "+"},

]
#add rule above
matcher.add("is_a_relationship", [pattern])
matches = matcher(doc)

spans = []
for _, start, end in matches:
    spans.append(doc[start:end])
spans= filter_spans(spans)

for span in spans:

    match_phrase = doc[span.start:span.end]
    subj = match_phrase[0]
    obj = match_phrase[3:]
    print(f"{subj.text} : {obj.text}")