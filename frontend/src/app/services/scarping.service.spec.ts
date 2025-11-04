import { TestBed } from '@angular/core/testing';

import { ScarpingService } from './scarping.service';

describe('ScarpingService', () => {
  let service: ScarpingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ScarpingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
