function isNotNull<T>(candidate: T|null): candidate is T {
  return candidate !== null;
}

interface Cite {
    citeTitle: string;
    citeDOI: string;
}

interface Article {
    Title: string;
    Journal: string;
    GCS: number;
    DOI: string;
    Year: number;
    Author: string;
    citeList: Cite[];
    LCR: number;
    LCS: number;
    localCiteList: Cite[];
    CR: number;
    Abstract: string;
    AuthorsList: string[];
}

function parseText(txt: string): Article[] {
  // eslint-disable-next-line no-control-regex
  const splitChunkMark = new RegExp('\n(?=PT J)', 'm');
  const chunks = txt.split(splitChunkMark).slice(1);
  const localArticleList: Article[] = chunks
    .map((each) => {
      // eslint-disable-next-line no-control-regex
      const splitLines = each.split(new RegExp('\n'));
      let TILineNum: number|undefined;
      let SOLineNum: number|undefined;
      let TCLineNum: number|undefined;
      let DILineNum: number|undefined;
      let PYLineNum: number|undefined;
      let AULineNum: number|undefined;
      let CRLineNum: number|undefined;
      let NRLineNum: number|undefined;
      let ABLineNum: number|undefined;
      let AFLineNum: number|undefined;
      splitLines.forEach((line, lineNum) => {
        switch (line.slice(0, 3)) {
          case 'TI ':
            TILineNum = lineNum;
            break;
          case 'SO ':
            SOLineNum = lineNum;
            break;
          case 'TC ':
            TCLineNum = lineNum;
            break;
          case 'DI ':
            DILineNum = lineNum;
            break;
          case 'PY ':
            PYLineNum = lineNum;
            break;
          case 'AU ':
            AULineNum = lineNum;
            break;
          case 'CR ':
            CRLineNum = lineNum;
            break;
          case 'NR ':
            NRLineNum = lineNum;
            break;
          case 'AB ':
            ABLineNum = lineNum;
            break;
          case 'AF ':
            AFLineNum = lineNum;
            break;
          default:
            break;
        }
      });
      if (
        typeof TILineNum !== 'undefined'
          && typeof SOLineNum !== 'undefined'
          && typeof TCLineNum !== 'undefined'
          && typeof DILineNum !== 'undefined'
          && typeof PYLineNum !== 'undefined'
          && typeof AULineNum !== 'undefined'
          && typeof CRLineNum !== 'undefined'
          && typeof NRLineNum !== 'undefined'
          && typeof ABLineNum !== 'undefined'
          && typeof AFLineNum !== 'undefined'
      ) {
        const TILines = splitLines.slice(TILineNum, SOLineNum);
        const TI = TILines.join(' ')
          .replace(new RegExp(' {4}', 'g'), ' ')
          .slice(3);

        const SOLine = splitLines[SOLineNum];
        const SO = SOLine.slice(3);

        const TCLine = splitLines[TCLineNum];
        const TC = parseInt(TCLine.slice(3), 10);

        const DILine = splitLines[DILineNum];
        const DI = DILine.slice(3);

        const PYLine = splitLines[PYLineNum];
        const PY = parseInt(PYLine.slice(3), 10);

        const AULine = splitLines[AULineNum];
        const AU = AULine.slice(3);

        const ABLine = splitLines[ABLineNum];
        const AB = ABLine.slice(3);

        const AFLines = splitLines.slice(AFLineNum, TILineNum);
        const AF = AFLines.map((line) => line.slice(3));

        const CRLines = splitLines.slice(CRLineNum, NRLineNum);

        const citeList: Cite[] = CRLines.map((citelineWithCap: string): Cite|null => {
          const citeLine = citelineWithCap.slice(3);
          const citeTitle = citeLine.split(new RegExp(', DOI '))[0];
          let citeDOI = citeLine.split(new RegExp(' DOI '))[1];
          if (citeTitle !== undefined && citeDOI !== undefined) {
            if (citeDOI.startsWith('[')) {
              citeDOI = citeDOI.split(',')[0].slice(1);
            }
            return { citeTitle, citeDOI };
          }
          return null;
        }).filter(isNotNull);
        return {
          Title: TI,
          Journal: SO,
          GCS: TC,
          DOI: DI,
          Year: PY,
          Author: AU,
          citeList,
          LCR: 0,
          LCS: 0,
          localCiteList: [],
          CR: citeList.length,
          Abstract: AB,
          AuthorsList: AF,
        };
      }
      return null;
    })
    .filter(isNotNull);
  return localArticleList;
}

function findLocalCite(rawArticles: Article[]): Article[] {
  const localArticleList = rawArticles;
  /* eslint no-param-reassign: ["error",
        { "props": true,
          "ignorePropertyModificationsFor": ["articleSource","cite","articleUse"]
        }] */
  localArticleList.forEach((articleUse) => {
    articleUse.citeList.forEach((cite) => {
      localArticleList.forEach((articleSource) => {
        if (cite.citeDOI === articleSource.DOI) {
          articleUse.LCR += 1;
          articleUse.localCiteList.push(cite);
          articleSource.LCS += 1;
        }
      });
    });
  });
  return localArticleList;
}

export {
  isNotNull, Article, parseText, findLocalCite,
};
